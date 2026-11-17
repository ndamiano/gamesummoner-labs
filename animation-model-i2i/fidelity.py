"""Pose fidelity: silhouette IoU of each edited frame vs its mannequin frame, plus foot-row drift.
usage: fidelity.py MANNEQUIN_DIR EDIT_DIR"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image

def mask(p, size):
    a = np.asarray(Image.open(p).convert("RGBA").resize(size))
    rgb = a[..., :3].astype(int)
    border = np.concatenate([rgb[:8].reshape(-1, 3), rgb[-8:].reshape(-1, 3), rgb[:, :8].reshape(-1, 3), rgb[:, -8:].reshape(-1, 3)])
    return np.abs(rgb - np.median(border, 0)).sum(-1) > 45

M, E = Path(sys.argv[1]), Path(sys.argv[2])
ious = []
for f in sorted(M.glob("frame_*.png")):
    e = E / f.name
    if not e.exists():
        continue
    size = Image.open(e).size
    m, o = mask(f, size), mask(e, size)
    iou = (m & o).sum() / (m | o).sum()
    ys_m, ys_o = np.where(m)[0], np.where(o)[0]
    xs_m, xs_o = np.where(m)[1], np.where(o)[1]
    ious.append(iou)
    print(f"{f.name} iou={iou:.3f} top={ys_o.min()-ys_m.min():+d} bottom={ys_o.max()-ys_m.max():+d} xmin={xs_o.min()-xs_m.min():+d} xmax={xs_o.max()-xs_m.max():+d}")
print(f"mean iou {np.mean(ious):.3f}")
