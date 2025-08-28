import os
import glob

# --- Configuration ---
# The base directory where your organized audio folders are
AUDIO_BASE_DIR = "./assets/audio"
# The final HTML file to be generated
OUTPUT_HTML_FILE = "./examples.html"

# The names of your subdirectories
INPUT_DIR = "inputs"
OURS_DIR = "ours"
BASELINE1_DIR = "pm2s"
BASELINE2_DIR = "midi2score"
GROUND_TRUTH_DIR = "ground_truth"

# Use an empty string for files that have no suffix (like inputs and ground truth)
FILENAME_SUFFIXES = {
    "input": "",
    "ours": "_perf_2_score",
    "base1": "_PM2S",
    "base2": "_MIDI2Score",
    "truth": ""
}

# --- HTML Template for a single sample ---

HTML_TEMPLATE = """
<div class="example-item sample-card bg-white p-6 rounded-xl shadow-lg border border-slate-200">
    <h4 class="text-xl font-semibold mb-6 text-slate-900">Sample {sample_id}: {sample_title}</h4>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 text-center mb-6">
        <div>
            <h5 class="font-medium mb-2">Input Performance</h5>
            <audio controls class="w-full"><source src="{input_path}" type="audio/wav"></audio>
        </div>
        <div>
            <h5 class="font-medium mb-2">Ground Truth Score</h5>
            <audio controls class="w-full"><source src="{truth_path}" type="audio/wav"></audio>
        </div>
    </div>
    <hr class="my-6">
    <div class="flex justify-center border-b border-slate-200 mb-4">
        <button data-target="ours-{sample_id}" class="tab-button active font-medium text-slate-800 py-2 px-4 rounded-t-lg">Our Model</button>
        <button data-target="base1-{sample_id}" class="tab-button font-medium text-slate-800 py-2 px-4 rounded-t-lg">Baseline 1 (PM2S)</button>
        <button data-target="base2-{sample_id}" class="tab-button font-medium text-slate-800 py-2 px-4 rounded-t-lg">Baseline 2 (MIDI2Score)</button>
    </div>
    <div class="text-center">
        <div id="ours-{sample_id}" class="tab-content"><audio controls class="w-full mx-auto max-w-md"><source src="{ours_path}" type="audio/wav"></audio></div>
        <div id="base1-{sample_id}" class="tab-content hidden"><audio controls class="w-full mx-auto max-w-md"><source src="{base1_path}" type="audio/wav"></audio></div>
        <div id="base2-{sample_id}" class="tab-content hidden"><audio controls class="w-full mx-auto max-w-md"><source src="{base2_path}" type="audio/wav"></audio></div>
    </div>
</div>
"""

def generate_html():
    """Finds all audio files and generates the examples.html content."""
    
    input_files = sorted(glob.glob(os.path.join(AUDIO_BASE_DIR, INPUT_DIR, "*.wav")))
    
    if not input_files:
        print(f"Error: No input files found in '{os.path.join(AUDIO_BASE_DIR, INPUT_DIR)}'. Please check your file structure.")
        return

    print(f"Found {len(input_files)} samples. Generating HTML...")
    
    all_examples_html = []
    valid_sample_counter = 0
    
    for i, input_path in enumerate(input_files):
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        
        # Create a more user-friendly title
        sample_title = base_name.title()
        
        # --- NEW: Construct paths using the base name and unique suffixes ---
        file_paths = {
            "sample_name": base_name,
            "sample_title": sample_title,
            "sample_id": i + 1,
            "input_path": os.path.join(AUDIO_BASE_DIR, INPUT_DIR, f"{base_name}{FILENAME_SUFFIXES['input']}.wav"),
            "ours_path": os.path.join(AUDIO_BASE_DIR, OURS_DIR, f"{base_name}{FILENAME_SUFFIXES['ours']}.wav"),
            "base1_path": os.path.join(AUDIO_BASE_DIR, BASELINE1_DIR, f"{base_name}{FILENAME_SUFFIXES['base1']}.wav"),
            "base2_path": os.path.join(AUDIO_BASE_DIR, BASELINE2_DIR, f"{base_name}{FILENAME_SUFFIXES['base2']}.wav"),
            "truth_path": os.path.join(AUDIO_BASE_DIR, GROUND_TRUTH_DIR, f"{base_name}{FILENAME_SUFFIXES['truth']}.wav"),
        }
        
        # Check if all files exist for this sample before adding it
        all_files_exist = all(os.path.exists(p) for p in [
            file_paths["ours_path"], file_paths["base1_path"], 
            file_paths["base2_path"], file_paths["truth_path"]
        ]) and base_name not in ["001_004", "1027_014", "968_026"]  # Exclude known problematic sample
        
        if all_files_exist:
            valid_sample_counter += 1
            file_paths["sample_id"] = valid_sample_counter
            all_examples_html.append(HTML_TEMPLATE.format(**file_paths))
        else:
            print(f"--> Warning: Skipping sample '{base_name}' because one or more corresponding output files are missing.")

    # Write the combined HTML to the output file
    with open(OUTPUT_HTML_FILE, 'w') as f:
        f.write('\n'.join(all_examples_html))
        
    print(f"\n✅ Successfully generated '{OUTPUT_HTML_FILE}' with {len(all_examples_html)} examples.")

if __name__ == "__main__":
    generate_html()