# Game Build & Packaging Automation (Python + Go)

This project is a Python-based automation script that scans a directory of Go game projects, copies them into a target folder, compiles their Go code, and generates a metadata file describing the available games.

It automates the process of managing multiple Go-based game projects in a structured and repeatable way.

---

## What This Project Does

The script performs the following tasks automatically:

1. Scans a source folder for game directories  
2. Identifies folders containing the word **"game"**  
3. Renames them by removing `_game` from the folder name  
4. Copies each game into a target folder  
5. Compiles the Go (`.go`) files inside each copied game folder  
6. Creates a `metadata.json` file listing all games and their count  

---
## How It Works

- The script searches for folders containing the word `"game"`.
- Each game folder is copied into the target directory.
- The `_game` suffix is removed from the folder name.
- Inside each copied folder, the script runs:

  ```bash
  go build <filename.go>
  ```

- A `metadata.json` file is created with:
  - List of game names  
  - Total number of games  


---

## Why This Project Is Useful

This project demonstrates:

- File system automation using Python  
- Integration with Go build tools  
- Subprocess handling  
- Build pipelines  
- Metadata generation  

It simulates how automation is used in real software build systems.

---

## Learning Source

This project was created as a **hands-on learning exercise** based on the following YouTube tutorial:

https://youtu.be/dQlw1Cdd3pw  

The script was written and adapted while practicing concepts from this tutorial.


