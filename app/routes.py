from flask import Blueprint, render_template, request
from app.services import scan_service
from app.repositories import scan_repository

main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@main.route("/scan", methods=["POST"])
def scan():
    url = request.form.get("url", "").strip()
    if not url:
        return render_template("index.html", error="Lütfen bir URL girin.")
    if not url.startswith("http"):
        url = "https://" + url

    result = scan_service.run_scan(url)

    if not result["success"]:
        return render_template("index.html", error=result["error"])

    return render_template(
        "result.html",
        scan=result["scan"],
        kvkk_items=result["kvkk_items"],
        gdpr_items=result["gdpr_items"]
    )


@main.route("/history")
def history():
    scans = scan_repository.get_all_scans()
    return render_template("history.html", scans=scans)


@main.route("/scan/<int:scan_id>")
def scan_detail(scan_id):
    scan = scan_repository.get_scan_by_id(scan_id)
    if not scan:
        return render_template("index.html", error="Tarama bulunamadı."), 404
    items = scan_repository.get_scan_items_by_scan_id(scan_id)
    kvkk_items = [i for i in items if i.category == "kvkk"]
    gdpr_items  = [i for i in items if i.category == "gdpr"]
    return render_template("scan_detail.html", scan=scan,
                           kvkk_items=kvkk_items, gdpr_items=gdpr_items)
