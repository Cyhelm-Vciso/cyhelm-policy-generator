from fastapi import FastAPI
from pydantic import BaseModel, Field


class OrganizationProfile(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    industry: str = Field(min_length=2, max_length=80)
    employees: int = Field(ge=1, le=1_000_000)
    cloud_services: list[str] = Field(default_factory=list, max_length=20)
    handles_payment_cards: bool = False
    remote_work: bool = True


class PolicyDraft(BaseModel):
    title: str
    status: str
    review_required: bool
    sections: dict[str, str]
    review_prompts: list[str]


def generate_policy(profile: OrganizationProfile) -> PolicyDraft:
    scope = (
        f"This policy applies to {profile.name}, its {profile.employees} personnel, "
        f"contractors, information assets, and approved service providers."
    )
    requirements = [
        "Access must follow least privilege and be reviewed at least quarterly.",
        "Security events must be reported immediately through the approved channel.",
        "Exceptions require documented risk acceptance, an owner, and an expiry date.",
    ]
    if profile.remote_work:
        requirements.append("Remote access must use approved devices, MFA, and encrypted channels.")
    if profile.handles_payment_cards:
        requirements.append("Payment-card data must remain within the approved PCI DSS scope.")
    if profile.cloud_services:
        requirements.append(
            "Cloud services in scope: " + ", ".join(sorted(set(profile.cloud_services))) + "."
        )
    return PolicyDraft(
        title=f"{profile.name} Information Security Policy",
        status="DRAFT — NOT APPROVED",
        review_required=True,
        sections={
            "purpose": f"Establish risk-based security direction for the {profile.industry} business.",
            "scope": scope,
            "policy": " ".join(requirements),
            "governance": "The accountable executive approves this policy; the security lead maintains it.",
            "review": "Review annually and after material business, threat, or regulatory change.",
        },
        review_prompts=[
            "Confirm legal and regulatory obligations with qualified counsel.",
            "Assign named owners and approval authority.",
            "Replace generic frequencies where risk assessment requires stronger controls.",
        ],
    )


app = FastAPI(title="CyHelm Virtual CISO Policy Generator", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/policies/information-security", response_model=PolicyDraft)
def information_security_policy(profile: OrganizationProfile) -> PolicyDraft:
    return generate_policy(profile)

