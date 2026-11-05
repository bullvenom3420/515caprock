# 515 Cap Rock Drive

Concept site for 515 Cap Rock Drive, Richardson, TX 75080. Static HTML, deployed on Vercel at 515caprock.com.

- `index.html`: the site (desktop scroll-to-rotate intro, phone intro video, touch/zoomable 3D model)
- `assets/frames`: 120 rotation frames, Huckleberry and the cat baked in
- `assets/pets`: clean window patches for the live idle-animation layer
- `assets/mobile`: phone intro video, poster, 3D model data and viewer
- `tools/`: model (`house.py`, built from the June 3, 2026 drawings), renderer, frame/patch export, page builder (`make_index.py`) and the pet drawings

Rebuild: `python3 tools/frames.py assets/frames 120 1600 1040 0 1`, then `python3 tools/make_index.py`.
