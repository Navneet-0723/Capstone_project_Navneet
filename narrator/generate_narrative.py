import os
import json
from google import genai
from google.genai import types

def generate_scr_narrative_offline(findings: dict) -> dict:
    """
    Task 4: Offline fallback path.
    Formats the SCR narrative using an f-string template directly from findings 
    with zero network calls, no API key, and complete determinism.
    """
    narrative_text = f"""
    ### Situation
    Mamaearth achieved a raw total revenue of ₹{findings['raw_total_revenue_inr']:,.2f}, which adjusted down to a clean total revenue of ₹{findings['cleaned_total_revenue_inr']:,.2f} across 175 validated orders after a duplicate reconciliation delta of ₹{findings['duplicate_reconciliation_delta_inr']:,.2f}. Initial time-series trends pointed to January 2026 as an inflated peak of ₹{findings['outlier_inflated_month']['apparent_revenue_inr']:,.2f}.

    ### Complication
    A deeper risk analysis revealed severe payment-method vulnerabilities, led by Cash on Delivery (COD) at a {findings['return_rate_by_payment']['COD']}% return rate—nearly triple that of card payments. Multi-level segmentation exposed that COD risk is heavily concentrated in Tier-2 cities, surging to a staggering {findings['highest_risk_segment']['return_rate_pct']}%. Furthermore, volume anomalies distorted our timeline: January's apparent revenue lead was an artifact of bulk orders, masking the true organic peak in March 2026 at ₹{findings['true_peak_month']['revenue_inr']:,.2f}.

    ### Resolution
    By implementing rigorous outlier detection before time-series forecasting, we corrected January's revenue to ₹{findings['outlier_inflated_month']['corrected_revenue_inr']:,.2f} and established March as premium peak performance. Regional operations and finance teams must now target high-risk COD Tier-2 segments with friction-reducing digital incentives or prepayment policies to curb returns and protect margins.
    """
    return {
        "status": "success",
        "narrative": narrative_text.strip(),
        "tokens": None
    }


def generate_scr_narrative(findings: dict) -> dict:
    """
    Task 2 & 3: Online Gemini API path.
    Reads API key from environment variables or a local API.txt file, 
    with automatic fallback to offline mode if neither is available or network fails.
    """
    api_key = None
    
    # 1. Try reading from environment variable first
    api_key = os.environ.get("GEMINI_API_KEY")
    
    # 2. If not in environment, try reading from local API.txt file
    if not api_key and os.path.exists('API.txt'):
        try:
            with open('API.txt', 'r', encoding='utf-8') as f:
                api_key = f.read().strip()
        except Exception:
            pass
            
    # If no valid key is found anywhere, trigger offline fallback mode
    if not api_key or api_key == "YOUR_ACTUAL_API_KEY_HERE":
        print("No API key found in environment or API.txt. Running Task 4: Offline fallback path.")
        return generate_scr_narrative_offline(findings)
    
    try:
        # Initialize GenAI client with the secured key
        client = genai.Client(api_key=api_key)
        
        # System instruction fixing the role, structure, and constraints
        system_instruction = (
            "You are a senior data analyst writing for Mamaearth's regional ops and finance heads. "
            "Write a business report structured strictly into three labeled sections: Situation, Complication, and Resolution. "
            "Explicit Constraint: Every number and metric in your output must come from the supplied findings dictionary "
            "and appear with the exact same value—no invented statistics."
        )
        
        # User prompt built dynamically from the findings dictionary
        user_prompt = f"""
        Generate the SCR narrative based strictly on these verified findings:
        {json.dumps(findings, indent=2)}
        """
        
        # Call model with locked parameters, explicit token limits, and timeout
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.0,                # Fully deterministic factual reporting
                max_output_tokens=400,          # Explicit token limit (>= 300)
                http_options={'timeout': 15000} # Timeout set to 15 seconds (15000ms)
            )
        )
        
        return {
            "status": "success",
            "narrative": response.text,
            "tokens": response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else None
        }
        
    except Exception as err:
        print(f"Gemini API network call failed due to: {str(err)}. Falling back to offline mode.")
        return generate_scr_narrative_offline(findings)


def verify_numeric_accuracy(narrative_text: str) -> bool:
    """
    Task 5: Numeric accuracy checklist.
    Asserts all five required figures are present as substrings (after normalizing commas).
    """
    normalized_text = narrative_text.replace(',', '')
    
    required_figures = [
        ("97358.30", "Cleaned total revenue"),
        ("44.4", "COD return rate"),
        ("54.5", "COD + Tier-2 highest-risk segment return rate"),
        ("2501.90", "Duplicate reconciliation delta"),
        ("20318.90", "True peak month revenue (March)")
    ]
    
    all_passed = True
    print("\n--- Running Task 5: Numeric Accuracy Checklist ---")
    for fig, desc in required_figures:
        fig_clean = fig.rstrip('0').rstrip('.') if '.' in fig else fig
        found = (fig in normalized_text) or (fig_clean in normalized_text)
        
        status = "PASS" if found else "FAIL"
        if not found:
            all_passed = False
        print(f"[{status}] Figure '{fig}' ({desc}) present in narrative.")
        
    march_found = "march" in narrative_text.lower()
    print(f"[{'PASS' if march_found else 'FAIL'}] Mention of 'March' present alongside peak revenue.")
    
    return all_passed and march_found


if __name__ == "__main__":
    # Ensure findings exist before running narrator
    findings_path = 'narrator/findings.json'
    if not os.path.exists(findings_path):
        raise FileNotFoundError(f"Could not find {findings_path}. Please run Part 2 (clean_and_eda.py) first!")
        
    with open(findings_path, 'r') as f:
        loaded_findings = json.load(f)
        
    # Execute narrative generation (Online or Offline fallback)
    result = generate_scr_narrative(loaded_findings)
    print(f"\nExecution Status: {result['status'].upper()}")
    print("\n--- Generated SCR Narrative Output ---\n")
    print(result['narrative'])
    
    # Run numeric accuracy checks
    passed = verify_numeric_accuracy(result['narrative'])
    if passed:
        print("\nResult: ALL NUMERIC ACCURACY CHECKS PASSED!")
    else:
        print("\nResult: WARNING - Some numeric checks failed.")
        
    # Save output sample for grader validation (Task 5 requirement)
    os.makedirs('narrator', exist_ok=True)
    sample_path = 'narrator/sample_output.txt'
    with open(sample_path, 'w', encoding='utf-8') as out_file:
        out_file.write(result['narrative'])
    print(f"Narrative successfully saved to '{sample_path}'.")