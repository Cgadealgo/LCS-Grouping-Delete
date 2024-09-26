from sortdelete import process_json, write_json_output

json_file = 'folder_hierarchy_large_ppt_data.json'  # Path to input JSON file
output_json_file = 'undeleted_files.json'  # Path to output JSON file

# Process the input JSON and get the list of undeleted files
kept_files = process_json(json_file)

# Write the undeleted files to a new JSON file
write_json_output(kept_files, output_json_file)
