import json
import re

def lcs(X, Y):
    m, n = len(X), len(Y)
    L = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i - 1] == Y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])

    return L[m][n]

# Function to compute similarity between two strings
def similarity_ratio(str1, str2):
    lcs_length = lcs(str1, str2)
    return lcs_length / max(len(str1), len(str2))

# Function to group filenames based on comparison to previous file only
def group_filenames_by_previous(filenames, threshold=0.9):
    if not filenames:
        return []

    groups = []
    current_group = [filenames[0]]

    for i in range(1, len(filenames)):
        previous_file = filenames[i - 1]
        current_file = filenames[i]
        if similarity_ratio(previous_file, current_file) >= threshold:
            current_group.append(current_file)
        else:
            groups.append(current_group)
            current_group = [current_file]

    # Add the last group
    if current_group:
        groups.append(current_group)

    return groups

# Function to filter filenames based on extensions
def filter_filenames(filenames):
    return [f for f in filenames if f.endswith(('.ppt', '.pptx'))]

# Function to sort filenames with numerical suffixes properly
def sort_filenames(filenames):
    def extract_number(filename):
        match = re.search(r'\((\d+)\)', filename)
        return int(match.group(1)) if match else 0

    def sort_key(filename):
        base_name = re.sub(r'\(\d+\)', '', filename)  # Remove numerical suffix
        return (base_name, extract_number(filename))

    return sorted(filenames, key=sort_key)

# Function to process the JSON and handle filenames
def process_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    updated_data = data.copy()  # Create a copy of the original data

    # Iterate over directories and process files
    for directory, content in data.items():
        filenames = content.get('files', [])

        # Filter filenames to include only .ppt or .pptx files
        filenames = filter_filenames(filenames)

        # Sort filenames considering numerical suffixes
        filenames = sort_filenames(filenames)

        # Group filenames based on comparison to previous file only
        grouped_files = group_filenames_by_previous(filenames)

        # Sort each group and keep only the last file
        kept_files = []
        for group in grouped_files:
            group.sort()  # Sort the group in ascending order
            if group:
                kept_file = group[-1]  # Keep only the last file
                kept_files.append(kept_file)

        # Update the original structure with the kept files
        updated_data[directory]['files'] = kept_files

    return updated_data

# Function to write the updated JSON structure to a file
def write_json_output(updated_data, output_file):
    with open(output_file, 'w') as outfile:
        json.dump(updated_data, outfile, indent=4)
    print(f"Updated file structure saved to {output_file}")

# Example usage
if __name__ == "__main__":
    json_file = 'folder_hierarchy_large_ppt_data.json'  # Replace with your input JSON file path
    output_json_file = 'undeleted_files.json'  # Output JSON file

    # Process the input JSON and get the updated structure
    updated_data = process_json(json_file)

    # Write the updated structure with undeleted files to a new JSON file
    write_json_output(updated_data, output_json_file)
