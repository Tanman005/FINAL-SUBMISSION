# Car Price Predictor — Deploy on Render

🔗 **Live demo:** https://car-price-predictor-osu4.onrender.com
💻 **Source code:** https://github.com/Tanman005/car_price_predictor-render-

## What's in this folder

| File | Purpose |
|---|---|
| `car_price_prediction.ipynb` | Trains the model, saves `model.pkl` + `columns.pkl` |
| `car_data.csv` | The real Car Dekho used-car dataset (301 listings) the model is trained on |
| `model.pkl` | Trained Random Forest regressor (R²≈0.96 on held-out data — already generated) |
| `columns.pkl` | Feature order + label encoders the app needs to match training-time encoding |
| `app.py` | Flask app: serves a web form (`/`) and a JSON API (`/api/predict`) |
| `templates/index.html` | The web form's HTML |
| `requirements.txt` | Exact pinned dependency versions |
| `render.yaml` | Render "Blueprint" config for one-click deploy |

## 1. About the dataset

`car_data.csv` is the well-known **Car Dekho used-car dataset** — 301 real used-car
listings scraped from cardekho.com, with columns `Car_Name`, `Year`, `Selling_Price`,
`Present_Price`, `Kms_Driven`, `Fuel_Type`, `Seller_Type`, `Transmission`, `Owner`.
The notebook drops `Car_Name` (too high-cardinality for 301 rows), converts `Year`
into `Car_Age`, and label-encodes the remaining categoricals. A Random Forest and a
Linear Regression are both trained and compared; the notebook keeps whichever
generalizes better on a held-out test split — currently Random Forest, at R²≈0.96.

**To swap in a different or larger dataset:** replace `car_data.csv` with your own
file of the same name and column layout, then re-run the whole notebook — it
overwrites `model.pkl` and `columns.pkl`, which `app.py` picks up automatically.

## 2. Test locally before deploying

```bash
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000` — fill the form and check you get a prediction.
Or hit the JSON API directly:

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"year":2019,"present_price":8.5,"kms_driven":35000,"fuel_type":"Petrol","seller_type":"Dealer","transmission":"Manual","owner":0}'
```

## 3. Push to GitHub

Render deploys from a Git repo, so this folder needs to be a repo first:

```bash
cd car-price-deploy
git init
git add .
git commit -m "Car price predictor - initial version"
```

Create an empty repo on GitHub (github.com → New repository), then:

```bash
git remote add origin https://github.com/<your-username>/<repo-name>.git
git branch -M main
git push -u origin main
```

## 4. Deploy on Render

**Option A — Blueprint (uses the included `render.yaml`, fewer clicks):**

1. Go to https://dashboard.render.com → **New** → **Blueprint**.
2. Connect your GitHub account if you haven't, then select the repo you just pushed.
3. Render reads `render.yaml` automatically and shows the `car-price-predictor`
   service it will create. Click **Apply**.
4. Wait for the build + deploy to finish (a few minutes on the free tier).

**Option B — Manual web service (if you'd rather not use the Blueprint file):**

1. Go to https://dashboard.render.com → **New** → **Web Service**.
2. Connect the GitHub repo.
3. Fill in:
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Free (or paid, if you want no cold starts)
4. Click **Create Web Service**.

## 5. Verify the live deployment

Once Render shows the service as "Live", it gives you a URL like
`https://car-price-predictor.onrender.com`. Check:

```bash
curl https://car-price-predictor.onrender.com/health
# {"status": "ok"}
```

Then open the URL in a browser to use the form, or POST to
`/api/predict` the same way you tested locally.

## Notes & gotchas

- **Free tier sleeps.** Render's free web services spin down after ~15 minutes of
  inactivity, so the first request after idle time takes 30–60s to "wake up." This
  is expected — not a bug in the app.
- **Model/library version mismatch.** `model.pkl` was saved with the exact
  scikit-learn/numpy/joblib versions pinned in `requirements.txt`. If you retrain
  locally with different versions installed, update `requirements.txt` to match
  (run `pip freeze | grep -E "scikit-learn|numpy|joblib"` and copy those exact
  versions in), or Render's environment may fail to unpickle the model.
- **Re-training:** if you edit the notebook and re-run it, `model.pkl` and
  `columns.pkl` are overwritten in place — just commit and push the updated files
  and Render will redeploy them on the next push (auto-deploy is on by default).
