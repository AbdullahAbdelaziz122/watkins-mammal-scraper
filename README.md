# WHOI Watkins Marine Mammal Sound Database Scraper

A Python tool designed to systematically scrape and archive audio data from the William A. Watkins Marine Mammal Sound Database hosted by the Woods Hole Oceanographic Institution (WHOI).

This script traverses the database by species, extracts download links, and organizes .wav files into local directories.

## ⚠️ Disclaimer & Ethical Use

**Please Read Before Using:**

- **This tool is for educational and research purposes only.** The data scraped by this tool belongs to the Woods Hole Oceanographic Institution and the original contributors.
- **Do not overwhelm the server.** This script runs sequentially, but please avoid running multiple instances simultaneously to prevent placing undue load on the WHOI servers.
- **Respect Copyright.** Do not redistribute the raw audio files commercially.
- **Cite the Data.** If you use this data for research, you must cite the Watkins Marine Mammal Sound Database (see Citation section below).

## Features

- **Automated Traversal:** Parses the main index to find all available species categories.
- **Organized Storage:** Creates a folder structure based on species common names (e.g., `whoi_whale_sounds/Blue Whale/`).
- **Resume Capability:** Checks if a file already exists locally before downloading, allowing you to restart the script without re-downloading existing files.
- **Error Handling:** Includes basic timeout and connection error handling.

## Prerequisites

- Python 3.6+


## Installation

1. Clone this repository:
```bash
git clone https://github.com/AbdullahAbdelaziz122/whoi-sound-scraper.git
cd whoi-sound-scraper
```

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the script directly from your terminal:
```bash
python whoi_scraper.py
```

## How it Works

1. The script fetches the main index page (`index.cfm`).
2. It parses the dropdown menu to identify all species (e.g., "Blue Whale", "Fin Whale").
3. It visits each species page to find the table of sound files.
4. It downloads .wav files into the `whoi_whale_sounds/` directory.

## Output Structure

After running, your directory will look like this:

```
whoi-sound-scraper/
│
├── scraper.py
├── whoi_whale_sounds/
│   ├── Blue Whale/
│   │   ├── 61025001.wav
│   │   └── 61025003.wav
│   ├── Fin Whale/
│   │   └── 61026001.wav
│   └── ...
```

## Citation

If you use the data retrieved by this script in a publication, WHOI requests the following citation format:

> Watkins, W. A., M. A. Daher, J. E. George, and D. Rodriguez. (2024). The William A. Watkins Marine Mammal Sound Database. Woods Hole Oceanographic Institution. Accessed via [Date] at https://cis.whoi.edu/science/B/whalesounds/index.cfm

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

MIT License