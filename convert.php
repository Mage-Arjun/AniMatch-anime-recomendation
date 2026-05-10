<?php
// convert.php — Converts a JSON/TXT file into a PHP script that outputs JSON

$source = 'Main_data.txt'; // your original file name
$target = 'Main_data.php'; // output PHP file

if (!file_exists($source)) {
    die("❌ Source file '$source' not found.");
}

// 1. Read your JSON or text data
$json = file_get_contents($source);

// 2. Try to decode it (to make sure it's valid JSON)
$data = json_decode($json, true);
if ($data === null) {
    die("❌ Invalid JSON! Please check your file format at https://jsonlint.com");
}

// 3. Generate PHP code
$phpCode = "<?php\n";
$phpCode .= "header('Content-Type: application/json');\n";
$phpCode .= "\$data = " . var_export($data, true) . ";\n";
$phpCode .= "echo json_encode(\$data, JSON_PRETTY_PRINT);\n";
$phpCode .= "?>";

// 4. Save the new PHP file
file_put_contents($target, $phpCode);

echo "✅ Conversion complete! File created: $target\n";
?>
