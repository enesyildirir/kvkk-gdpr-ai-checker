class ScanItem:
    """Bir taramadaki tek bir kontrol maddesini temsil eder."""

    def __init__(self, id=None, scan_id=None, category=None,
                 item_key=None, item_label=None, status=0):
        self.id = id
        self.scan_id = scan_id
        self.category = category      # "kvkk" veya "gdpr"
        self.item_key = item_key      # örn: "has_privacy_policy"
        self.item_label = item_label  # örn: "Gizlilik politikası mevcut"
        self.status = status          # 1: geçti, 0: geçmedi

    def to_dict(self):
        return {
            "id": self.id,
            "scan_id": self.scan_id,
            "category": self.category,
            "item_key": self.item_key,
            "item_label": self.item_label,
            "status": self.status
        }
