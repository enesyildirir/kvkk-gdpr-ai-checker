class Scan:
    """Bir tarama işlemini temsil eder."""

    def __init__(self, id=None, url=None, kvkk_score=0.0, gdpr_score=0.0,
                 risk_level=None, llm_suggestions=None, created_at=None):
        self.id = id
        self.url = url
        self.kvkk_score = kvkk_score
        self.gdpr_score = gdpr_score
        self.risk_level = risk_level
        self.llm_suggestions = llm_suggestions
        self.created_at = created_at

    def to_dict(self):
        return {
            "id": self.id,
            "url": self.url,
            "kvkk_score": self.kvkk_score,
            "gdpr_score": self.gdpr_score,
            "risk_level": self.risk_level,
            "llm_suggestions": self.llm_suggestions,
            "created_at": str(self.created_at)
        }
