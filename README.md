# ChaatGPT
An open-source AI ChaatBot designed for the Musem of the Moving Image
A fun quiz that matches you with your perfect chaat — powered by AI running on your own computer.

---

## Get Started

### 1. Install Ollama

Go to [ollama.com](https://ollama.com) and download the app for your computer (Mac or Windows).

### 2. Download a Model

Open the Ollama app and find Llama3.2 and download.
Alternatively, open Terminal (Mac) or PowerShell (Windows) and run:

```
ollama pull llama3.2
```

This downloads the AI model (~2GB). Wait for it to finish.

### 3. Run the Quiz

In Terminal or PowerShell, navigate to the folder containing `chaatgpt.py` and run:

```
python3 chaatgpt.py
```

On Windows, you may need to use `python` instead of `python3`.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Ollama not running" | Open the Ollama app, or run `ollama serve` in a separate terminal |
| "python not found" | Install Python from [python.org](https://python.org) |
| Slow first response | Normal — the model takes a moment to load the first time |

---

## Resources

- [Ollama](https://ollama.com) — Run AI models locally
- [Ollama Model Library](https://ollama.com/library) — Browse available models
- [Silsila (1981)](https://en.wikipedia.org/wiki/Silsila_(1981_film)) — The Bollywood classic referenced in the quiz
- [Rang Barse](https://www.youtube.com/watch?v=bnMbHknPMqI) — The iconic Holi song from the film
