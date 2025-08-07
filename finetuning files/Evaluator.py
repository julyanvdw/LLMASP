import tempfile
import os
import io
import sys
import subprocess
import json
from pathlib import Path
from contextlib import redirect_stderr, redirect_stdout
from typing import Dict, List, Optional
from datetime import datetime

class CNLToASPEvaluator:
    """
    CNL → ASP evaluator using conda clingo for robust syntax validation and semantic equivalence
    """
    
    def __init__(self, enable_semantic=True, verbose=False):
        """
        Initialize CNL → ASP evaluator
        
        Args:
            enable_semantic: Whether to enable semantic equivalence checking
            verbose: Whether to print status messages during initialization
        """
        self.enable_semantic = enable_semantic
        self.verbose = verbose
        self.clingo_available = self._check_clingo()
        self.clingo_timeout = 10  # seconds
        
        if not self.clingo_available:
            raise RuntimeError(
                "Clingo is required for ASP evaluation but not available. "
                "Please install with: conda install -c potassco clingo"
            )
    
    def _check_clingo(self) -> bool:
        """Check if conda clingo is available"""
        try:
            import clingo
            if self.verbose:
                version = getattr(clingo, '__version__', 'unknown')
                print(f"✅ Clingo {version} available via conda")
            return True
        except ImportError:
            if self.verbose:
                print("❌ Clingo not available - install with: conda install -c potassco clingo")
            return False
    
    def _capture_clingo_errors(self, asp_code: str) -> Dict:
        """Capture clingo errors silently but store them for later reporting"""
        if not asp_code.strip():
            return {
                'valid': False, 
                'error_message': 'Empty ASP code',
                'clingo_errors': [],
                'method': 'empty_check'
            }
        
        try:
            import clingo
            
            # Capture both stdout and stderr
            captured_stdout = io.StringIO()
            captured_stderr = io.StringIO()
            
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            
            try:
                sys.stdout = captured_stdout
                sys.stderr = captured_stderr
                
                ctl = clingo.Control(['--warn=none'])
                ctl.add("base", [], asp_code)
                ctl.ground([("base", [])])
                is_valid = True
                error_details = []
                
            except Exception as e:
                is_valid = False
                # Parse the captured errors plus exception
                error_output = captured_stdout.getvalue() + captured_stderr.getvalue() + str(e)
                error_details = self._parse_clingo_errors(error_output)
                
            finally:
                sys.stdout = old_stdout
                sys.stderr = old_stderr
            
            return {
                'valid': is_valid,
                'error_message': error_details[0] if error_details else None,
                'clingo_errors': error_details,
                'method': 'clingo_python'
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error_message': str(e),
                'clingo_errors': [str(e)],
                'method': 'error'
            }
    
    def _run_clingo_subprocess(self, asp_code: str, facts=""):
        """Run ASP code through Clingo subprocess and get answer sets"""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.lp', delete=False) as f:
                f.write(facts + "\n" + asp_code)
                temp_file = f.name
            
            # Run Clingo
            result = subprocess.run(
                ['clingo', temp_file, '--outf=2'],  # JSON output format
                capture_output=True,
                text=True,
                timeout=self.clingo_timeout
            )
            
            Path(temp_file).unlink()  # Clean up
            
            # Clingo return codes: 10=SATISFIABLE, 20=UNSATISFIABLE, 30=UNKNOWN/SATISFIABLE
            if result.returncode not in [10, 20, 30]:
                return None, f"Clingo error (code {result.returncode}): {result.stderr}"
            
            # Parse JSON output
            if not result.stdout.strip():
                return [], None  # No models (unsatisfiable)
            
            try:
                output = json.loads(result.stdout)
            except json.JSONDecodeError as e:
                return None, f"JSON parse error: {e}"
            
            answer_sets = []
            
            # Extract answer sets from all calls
            for call in output.get('Call', []):
                for witness in call.get('Witnesses', []):
                    answer_set = set(witness.get('Value', []))
                    answer_sets.append(answer_set)
            
            return answer_sets, None
            
        except subprocess.TimeoutExpired:
            return None, "Timeout"
        except Exception as e:
            return None, f"Error: {str(e)}"
    
    def _parse_clingo_errors(self, error_text: str) -> List[str]:
        """Parse clingo error text into readable format"""
        errors = []
        lines = error_text.split('\n')
        
        current_error = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Main error lines
            if 'error:' in line:
                if 'syntax error' in line:
                    current_error = f"🔴 Syntax Error: {line.split('error:')[1].strip()}"
                elif 'lexer error' in line:
                    current_error = f"🔴 Lexer Error: {line.split('error:')[1].strip()}"
                elif 'unsafe variables' in line:
                    current_error = f"⚠️ Unsafe Variables: {line.split('error:')[1].strip()}"
                else:
                    current_error = f"❌ Error: {line.split('error:')[1].strip()}"
                errors.append(current_error)
                
            # Additional context lines
            elif 'note:' in line:
                note = f"   📝 Note: {line.split('note:')[1].strip()}"
                errors.append(note)
            elif 'info:' in line:
                info = f"   ℹ️ Info: {line.split('info:')[1].strip()}"
                errors.append(info)
            elif line.startswith('<block>') and ':' in line:
                # Location information
                location = f"   📍 Location: {line}"
                errors.append(location)
        
        return errors[:10]  # Limit to first 10 error lines for readability
    
    def check_syntax(self, asp_code: str) -> Dict:
        """
        Check if ASP code is syntactically valid using clingo (silently)
        
        Args:
            asp_code: ASP code string to validate
            
        Returns:
            Dict with validation results and captured errors
        """
        return self._capture_clingo_errors(asp_code)
    
    def check_semantic_equivalence(self, target: str, predicted: str, facts="") -> Dict:
        """
        Check semantic equivalence between target and predicted ASP code using answer sets
        
        Args:
            target: Expected ASP code
            predicted: Model-generated ASP code
            facts: Additional facts to use as context
            
        Returns:
            Dict with 'equivalent' (bool), 'reason' (str), additional analysis
        """
        if not self.enable_semantic:
            return {
                'equivalent': False,
                'reason': 'Semantic checking disabled',
                'method': 'disabled'
            }
        
        # Get answer sets for both
        target_sets, target_error = self._run_clingo_subprocess(target, facts)
        pred_sets, pred_error = self._run_clingo_subprocess(predicted, facts)
        
        # Handle errors
        if target_error:
            return {
                'equivalent': False,
                'reason': f"Target error: {target_error}",
                'method': 'clingo_subprocess',
                'target_error': target_error,
                'predicted_error': pred_error
            }
        if pred_error:
            return {
                'equivalent': False,
                'reason': f"Predicted error: {pred_error}",
                'method': 'clingo_subprocess',
                'target_error': target_error,
                'predicted_error': pred_error
            }
        
        # Compare answer sets
        if target_sets == pred_sets:
            return {
                'equivalent': True,
                'reason': 'Semantically equivalent (identical answer sets)',
                'method': 'clingo_subprocess',
                'target_sets': len(target_sets),
                'predicted_sets': len(pred_sets)
            }
        
        # Check if answer sets match (order independent)
        target_sorted = sorted([sorted(list(s)) for s in target_sets])
        pred_sorted = sorted([sorted(list(s)) for s in pred_sets])
        
        if target_sorted == pred_sorted:
            return {
                'equivalent': True,
                'reason': 'Semantically equivalent (same answer sets, different order)',
                'method': 'clingo_subprocess',
                'target_sets': len(target_sets),
                'predicted_sets': len(pred_sets)
            }
        
        return {
            'equivalent': False,
            'reason': f'Different answer sets: target has {len(target_sets)}, predicted has {len(pred_sets)}',
            'method': 'clingo_subprocess',
            'target_sets': len(target_sets),
            'predicted_sets': len(pred_sets),
            'target_answer_sets': target_sets,
            'predicted_answer_sets': pred_sets
        }
    
    def _normalize_whitespace(self, text: str) -> str:
        """Basic whitespace normalization only"""
        return ' '.join(text.split()).strip()
    
    def _generate_error_cases_summary(self, detailed_results: List[Dict]) -> str:
        """Generate detailed error cases to display at the top"""
        syntax_error_cases = []
        semantic_error_cases = []
        
        for result in detailed_results:
            test_case = result['test_case']
            target = result['target']
            predicted = result['predicted']
            
            # Syntax errors (non-empty but syntactically invalid)
            if not result['syntax_valid'] and result['non_empty']:
                error_msg = result['syntax_info'].get('error_message', 'Unknown syntax error')
                syntax_error_cases.append(f"""
🔴 Test {test_case} - SYNTAX ERROR
   Target:    {target}
   Predicted: {predicted}
   Error:     {error_msg}""")
            
            # Semantic errors (syntax valid but semantically wrong)
            if (result['syntax_valid'] and 
                not result['semantic_match'] and 
                result['non_empty'] and 
                self.enable_semantic):
                reason = result.get('semantic_info', {}).get('reason', 'Unknown semantic error')
                semantic_error_cases.append(f"""
❌ Test {test_case} - SEMANTIC ERROR
   Target:    {target}
   Predicted: {predicted}
   Issue:     {reason}""")
        
        summary_parts = []
        
        if syntax_error_cases or semantic_error_cases:
            summary_parts.append("🚨 ERROR CASES SUMMARY")
            summary_parts.append("=" * 80)
        
        if syntax_error_cases:
            summary_parts.extend(syntax_error_cases[:15])  # Limit to first 15 for readability
            if len(syntax_error_cases) > 15:
                summary_parts.append(f"\n... and {len(syntax_error_cases) - 15} more syntax errors")
        
        if semantic_error_cases:
            summary_parts.extend(semantic_error_cases[:15])  # Limit to first 15
            if len(semantic_error_cases) > 15:
                summary_parts.append(f"\n... and {len(semantic_error_cases) - 15} more semantic errors")
        
        if syntax_error_cases or semantic_error_cases:
            summary_parts.append("=" * 80)
            summary_parts.append("")
        else:
            summary_parts.append("✅ NO SYNTAX OR SEMANTIC ERRORS DETECTED\n")
        
        return '\n'.join(summary_parts)
    
    def evaluate(self, predictions: List[str], targets: List[str]) -> Dict:
        """
        Comprehensive evaluation of ASP predictions with semantic equivalence
        
        Args:
            predictions: List of model-generated ASP code
            targets: List of expected ASP code
            
        Returns:
            Dict containing evaluation metrics and detailed results
        """
        if len(predictions) != len(targets):
            raise ValueError(f"Predictions ({len(predictions)}) and targets ({len(targets)}) must have same length")
        
        results = {
            'total': len(predictions),
            'exact_matches': 0,
            'syntax_valid': 0,
            'semantic_matches': 0,
            'non_empty': 0,
            'detailed_results': [],
            'task_type': 'cnl-asp'
        }
        
        for i, (pred, target) in enumerate(zip(predictions, targets)):
            # Basic non-empty check
            is_non_empty = bool(pred.strip())
            if is_non_empty:
                results['non_empty'] += 1
            
            # Exact match (only whitespace normalized)
            pred_norm = self._normalize_whitespace(pred)
            target_norm = self._normalize_whitespace(target)
            is_exact_match = pred_norm.lower() == target_norm.lower()
            if is_exact_match:
                results['exact_matches'] += 1
            
            # Syntax validation using clingo (silent)
            syntax_result = self.check_syntax(pred)
            is_syntax_valid = syntax_result['valid']
            if is_syntax_valid:
                results['syntax_valid'] += 1
            
            # Also check target syntax for debugging
            target_syntax_result = self.check_syntax(target)
            
            # Semantic equivalence using answer sets
            semantic_result = None
            is_semantic_match = False
            if self.enable_semantic and is_syntax_valid:  # Only check semantics if syntax is valid
                semantic_result = self.check_semantic_equivalence(target, pred)
                is_semantic_match = semantic_result['equivalent']
                if is_semantic_match:
                    results['semantic_matches'] += 1
            elif self.enable_semantic:
                # Syntax invalid, so semantics can't be checked
                semantic_result = {
                    'equivalent': False,
                    'reason': 'Cannot check semantics: syntax invalid',
                    'method': 'skipped_due_to_syntax'
                }
            
            # Error classification
            error_type = self._classify_error(
                pred, target, is_exact_match, is_syntax_valid, is_semantic_match, syntax_result
            )
            
            # Store detailed result with all clingo analysis
            result_detail = {
                'test_case': i + 1,
                'target': target,
                'predicted': pred,
                'exact_match': is_exact_match,
                'syntax_valid': is_syntax_valid,
                'semantic_match': is_semantic_match,
                'non_empty': is_non_empty,
                'error_type': error_type,
                'syntax_info': syntax_result,
                'semantic_info': semantic_result,
                'target_syntax_valid': target_syntax_result['valid'],
                'target_syntax_info': target_syntax_result
            }
            
            # Add clingo analysis for results file
            if syntax_result.get('clingo_errors'):
                result_detail['clingo_analysis'] = {
                    'predicted_errors': syntax_result['clingo_errors'],
                    'error_count': len(syntax_result['clingo_errors'])
                }
            
            if target_syntax_result.get('clingo_errors'):
                if 'clingo_analysis' not in result_detail:
                    result_detail['clingo_analysis'] = {}
                result_detail['clingo_analysis']['target_errors'] = target_syntax_result['clingo_errors']
                result_detail['clingo_analysis']['target_error_count'] = len(target_syntax_result['clingo_errors'])
            
            results['detailed_results'].append(result_detail)
        
        # Calculate rates
        results.update({
            'exact_match_rate': results['exact_matches'] / results['total'],
            'syntax_valid_rate': results['syntax_valid'] / results['total'],
            'semantic_match_rate': results['semantic_matches'] / results['total'],
            'non_empty_rate': results['non_empty'] / results['total']
        })
        
        # Add error cases summary
        results['error_cases_summary'] = self._generate_error_cases_summary(results['detailed_results'])
        
        return results
    
    def _classify_error(self, predicted: str, target: str, exact_match: bool, 
                       syntax_valid: bool, semantic_match: bool, syntax_result: Dict) -> Optional[str]:
        """Classify the type of error for debugging purposes"""
        if exact_match:
            return None
        
        if not predicted.strip():
            return "empty_output"
        
        if not syntax_valid:
            # More specific error classification based on clingo errors
            errors = syntax_result.get('clingo_errors', [])
            for error in errors:
                if 'lexer error' in error.lower():
                    return "lexer_error"
                elif 'syntax error' in error.lower():
                    return "syntax_error"
                elif 'unsafe variables' in error.lower():
                    return "unsafe_variables"
            return "syntax_error"
        
        if semantic_match:
            return "semantic_equivalent"
        
        return "semantic_error"
    
    def get_evaluation_summary(self, results: Dict) -> str:
        """Generate a human-readable summary of evaluation results with 4 key metrics"""
        summary = []
        summary.append(f"📊 CNL→ASP Evaluation Summary ({results['total']} examples)")
        summary.append("")
        
        # Add error cases summary at the top
        if results.get('error_cases_summary'):
            summary.append(results['error_cases_summary'])
        
        # 4 KEY METRICS in order of importance
        summary.append("📊 PERFORMANCE METRICS")
        summary.append("──────────────────────────────────────────────────")
        summary.append(f"1️⃣ Syntax Valid:   {results['syntax_valid_rate']:.1%} ({results['syntax_valid']}/{results['total']})")
        
        if self.enable_semantic:
            summary.append(f"2️⃣ Semantic Match: {results['semantic_match_rate']:.1%} ({results['semantic_matches']}/{results['total']})")
        
        summary.append(f"3️⃣ Exact Match:    {results['exact_match_rate']:.1%} ({results['exact_matches']}/{results['total']})")
        summary.append(f"4️⃣ Non-empty:      {results['non_empty_rate']:.1%} ({results['non_empty']}/{results['total']})")
        summary.append("")
        
        return '\n'.join(summary)
    
    def save_evaluation_report(self, results: Dict, output_path: str, metadata: Dict = None):
        """
        Save comprehensive evaluation report to file
        
        Args:
            results: Evaluation results from evaluate()
            output_path: Path to save the report file
            metadata: Optional metadata (checkpoint info, etc.)
        """
        with open(output_path, 'w') as f:
            # Write header with metadata
            f.write("=" * 80 + "\n")
            f.write("📋 ASP EVALUATION REPORT\n")
            f.write("=" * 80 + "\n")
            f.write(f"🕒 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            if metadata:
                if 'construct_name' in metadata:
                    f.write(f"📋 Target Construct: {metadata['construct_name']}\n")
                if 'checkpoint_path' in metadata:
                    f.write(f"🔧 Checkpoint Path: {metadata['checkpoint_path']}\n")
                if 'data_path' in metadata:
                    f.write(f"📁 Data Path: {metadata['data_path']}\n")
                if 'test_examples' in metadata:
                    f.write(f"🧪 Test Examples: {metadata['test_examples']}\n")
            
            f.write("\n")
            
            # Write summary with error cases and metrics
            f.write(self.get_evaluation_summary(results))
            f.write("\n\n")
            
            # Write all detailed test cases
            f.write("📋 INDIVIDUAL TEST CASES (FULL OUTPUT)\n")
            f.write("=" * 80 + "\n\n")
            
            for result in results['detailed_results']:
                # Status indicator
                if result['exact_match']:
                    status = "✅ EXACT MATCH"
                elif result['semantic_match'] and self.enable_semantic:
                    status = "🎯 SEMANTIC MATCH"
                elif result['syntax_valid']:
                    status = "🔧 SYNTAX VALID"
                elif result['non_empty']:
                    status = "❌ SYNTAX ERROR"
                else:
                    status = "🔴 EMPTY OUTPUT"
                
                f.write(f"{status} - Test Case {result['test_case']}\n")
                f.write("─" * 76 + "\n")
                f.write(f"INPUT:\n")
                # Note: We don't have input here, would need to be passed in
                f.write(f"\nTARGET:\n┌{'─' * 76}>\n│ {result['target']:<74} >\n└{'─' * 76}>\n")
                f.write(f"\nPREDICTED:\n┌{'─' * 76}>\n│ {result['predicted']:<74} >\n└{'─' * 76}>\n")
                f.write(f"\n📏 Lengths: Target={len(result['target'])} chars, Predicted={len(result['predicted'])} chars\n")
                
                # Analysis
                f.write(f"\n🔍 Analysis:\n")
                f.write(f"   ✅ Exact Match:    {result['exact_match']}\n")
                f.write(f"   🔧 Syntax Valid:   {result['syntax_valid']}\n")
                f.write(f"   🎯 Semantic Match: {result['semantic_match']}\n")
                f.write(f"   📝 Non-empty:      {result['non_empty']}\n")
                
                if result.get('error_type'):
                    f.write(f"   ⚠️ Error Type:     {result['error_type']}\n")
                
                if result.get('clingo_analysis'):
                    f.write(f"   🔍 Clingo Analysis: {result['clingo_analysis']}\n")
                
                f.write("\n")


class NLToCNLEvaluator:
    """
    NL → CNL evaluator for natural language to controlled natural language translation
    """
    
    def __init__(self):
        """Initialize NL → CNL evaluator"""
        pass
    
    def evaluate(self, predictions: List[str], targets: List[str]) -> Dict:
        """
        Evaluate natural language predictions
        
        Args:
            predictions: List of model-generated CNL
            targets: List of expected CNL
            
        Returns:
            Dict containing evaluation metrics and detailed results
        """
        if len(predictions) != len(targets):
            raise ValueError(f"Predictions ({len(predictions)}) and targets ({len(targets)}) must have same length")
        
        results = {
            'total': len(predictions),
            'exact_matches': 0,
            'non_empty': 0,
            'detailed_results': [],
            'task_type': 'nl-cnl'
        }
        
        for i, (pred, target) in enumerate(zip(predictions, targets)):
            # Basic checks
            is_non_empty = bool(pred.strip())
            if is_non_empty:
                results['non_empty'] += 1
            
            # Case-insensitive exact match (whitespace normalized)
            pred_norm = ' '.join(pred.split()).strip().lower()
            target_norm = ' '.join(target.split()).strip().lower()
            is_exact_match = pred_norm == target_norm
            if is_exact_match:
                results['exact_matches'] += 1
            
            # Store detailed result
            results['detailed_results'].append({
                'test_case': i + 1,
                'target': target,
                'predicted': pred,
                'exact_match': is_exact_match,
                'non_empty': is_non_empty,
                'error_type': None if is_exact_match else ('empty_output' if not is_non_empty else 'content_mismatch')
            })
        
        # Calculate rates
        results.update({
            'exact_match_rate': results['exact_matches'] / results['total'],
            'non_empty_rate': results['non_empty'] / results['total']
        })
        
        return results
    
    def get_evaluation_summary(self, results: Dict) -> str:
        """Generate a human-readable summary of evaluation results"""
        summary = []
        summary.append(f"📊 NL→CNL Evaluation Summary ({results['total']} examples)")
        summary.append(f"✅ Exact Match: {results['exact_match_rate']:.1%} ({results['exact_matches']}/{results['total']})")
        summary.append(f"📝 Non-empty: {results['non_empty_rate']:.1%} ({results['non_empty']}/{results['total']})")
        
        return '\n'.join(summary)
    
    def save_evaluation_report(self, results: Dict, output_path: str, metadata: Dict = None):
        """Save evaluation report for NL→CNL task"""
        with open(output_path, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("📋 NL→CNL EVALUATION REPORT\n") 
            f.write("=" * 80 + "\n")
            f.write(f"🕒 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write(self.get_evaluation_summary(results))
            f.write("\n\n")
            
            # Detailed cases
            for result in results['detailed_results']:
                status = "✅ MATCH" if result['exact_match'] else "❌ MISMATCH"
                f.write(f"{status} - Test Case {result['test_case']}\n")
                f.write(f"Target:    {result['target']}\n")
                f.write(f"Predicted: {result['predicted']}\n\n")


def create_evaluator(task_type: str, **kwargs):
    """
    Factory function to create appropriate evaluator based on task type
    
    Args:
        task_type: 'cnl-asp'/'asp' for CNL→ASP or 'nl-cnl'/'nl' for NL→CNL
        **kwargs: Additional arguments passed to evaluator
        
    Returns:
        Appropriate evaluator instance
    """
    task_lower = task_type.lower()
    
    if task_lower in ['cnl-asp', 'asp']:
        return CNLToASPEvaluator(**kwargs)
    elif task_lower in ['nl-cnl', 'nl']:
        return NLToCNLEvaluator(**kwargs)
    else:
        raise ValueError(f"Unknown task type: {task_type}. Use 'cnl-asp', 'asp', 'nl-cnl', or 'nl'")


def test_file_output():
    """Test the evaluator's file output functionality"""
    print("🧪 Testing Evaluator File Output")
    print("=" * 50)
    
    try:
        evaluator = CNLToASPEvaluator(enable_semantic=True, verbose=True)
        
        # Test cases
        predictions = [
            'person("alice"). person("bob").',    # Exact match
            'person("bob"). person("alice").',    # Semantic equivalent
            'animal("dog").',                     # Syntax valid, semantically different
            'person("alice"',                     # Syntax error
            '',                                   # Empty
        ]
        
        targets = [
            'person("alice"). person("bob").',
            'person("alice"). person("bob").',
            'person("alice").',
            'person("alice").',
            'person("alice").',
        ]
        
        results = evaluator.evaluate(predictions, targets)
        
        # Test file output with metadata
        metadata = {
            'construct_name': 'test_facts',
            'checkpoint_path': 'test/model/path',
            'data_path': 'test/data/path',
            'test_examples': len(predictions)
        }
        
        output_path = "test_evaluation_report.txt"
        evaluator.save_evaluation_report(results, output_path, metadata)
        
        print(f"✅ Report saved to: {output_path}")
        print("\n📊 Console Summary:")
        print(evaluator.get_evaluation_summary(results))
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_file_output()
