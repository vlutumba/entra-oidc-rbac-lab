# Entra ID OIDC RBAC Lab

## Overview

The Entra ID OIDC RBAC Lab is a hands-on Identity and Access Management (IAM) project demonstrating authentication, authorization, and Role-Based Access Control (RBAC) using Microsoft Entra ID (formerly Azure Active Directory), OpenID Connect (OIDC), Flask, and Python.

This project simulates how enterprise applications authenticate users through Microsoft Entra ID and authorize access based on group membership.

---

# Objectives

This project demonstrates:

* Microsoft Entra ID Authentication
* OpenID Connect (OIDC)
* OAuth 2.0 Authorization Flow
* JWT Token Processing
* User Claims Retrieval
* Group Claims Retrieval
* Role-Based Access Control (RBAC)
* Flask Session Management
* Enterprise Authentication Concepts

---

# Architecture

```text
+--------------------+
| Microsoft Entra ID |
+---------+----------+
          |
          | OIDC Authentication
          |
          v
+--------------------+
| Flask Application  |
+---------+----------+
          |
          +----------------+
          |                |
          v                v
+----------------+  +----------------+
| Dashboard Page |  | Admin Page     |
+----------------+  +----------------+
                         |
                         |
                  IAM-Admins Only
```

---

# Technologies Used

## Identity Provider

* Microsoft Entra ID

## Authentication Protocol

* OpenID Connect (OIDC)
* OAuth 2.0

## Application

* Python
* Flask
* MSAL (Microsoft Authentication Library)

## Security

* JWT Tokens
* RBAC
* Group Claims
* Secure Sessions

---

# Azure Configuration

## Step 1 – Create Application Registration

Created application:

```text
Entra ID OIDC RBAC Lab
```

Configuration:

```text
Single Tenant
```

Redirect URI:

```text
http://localhost:5000/getAToken
```

---

## Step 2 – Create Client Secret

Created:

```text
Certificates & Secrets
→ New Client Secret
```

Used by Flask application to authenticate with Microsoft Entra ID.

---

## Step 3 – Create Security Groups

Created:

```text
IAM-Admins
IAM-Analysts
```

Purpose:

* IAM-Admins = Administrative Access
* IAM-Analysts = Standard IAM Access

Membership Type:

```text
Assigned
```

Group Type:

```text
Security
```

---

## Step 4 – Add User Membership

Added test account to:

```text
IAM-Admins
IAM-Analysts
```

---

# Token Configuration

## Group Claims

Configured:

```text
App Registration
→ Token Configuration
→ Add Groups Claim
```

Selected:

```text
Security Groups
```

Result:

Group membership information is included in issued tokens.

Example:

```json
"groups": [
  "20bc64d1-fc89-40bb-871e-47602508d99b",
  "096af11e-ca54-4eb6-8a78-0903fef7048f"
]
```

---

## Optional Claims

Added:

```text
email
family_name
given_name
preferred_username
```

Purpose:

Provide user identity information to the application.

Example:

```json
{
  "name": "Vilfride Lutumba",
  "email": "triplev3@hotmail.com",
  "preferred_username": "triplev3@hotmail.com"
}
```

---

# Local Development Setup

## Create Virtual Environment

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install flask
pip install msal
pip install python-dotenv
pip install requests
```

Generate requirements:

```bash
pip freeze > requirements.txt
```

---

# Environment Variables

File:

```text
.env
```

Configuration:

```env
CLIENT_ID=<Application Client ID>

TENANT_ID=<Tenant ID>

CLIENT_SECRET=<Client Secret>

REDIRECT_URI=http://localhost:5000/getAToken

FLASK_SECRET_KEY=<Random Secret>

IAM_ADMINS_GROUP_ID=20bc64d1-fc89-40bb-871e-47602508d99b

IAM_ANALYSTS_GROUP_ID=096af11e-ca54-4eb6-8a78-0903fef7048f
```

---

# Authentication Flow

1. User browses to application.
2. User clicks Login with Microsoft.
3. Application redirects to Microsoft Entra ID.
4. User authenticates.
5. Microsoft Entra ID issues an ID Token.
6. Flask validates the token.
7. User claims are stored in session.
8. Application authorizes access based on group membership.

---

# Claims Successfully Retrieved

Example token:

```json
{
  "name": "Vilfride Lutumba",
  "email": "triplev3@hotmail.com",
  "preferred_username": "triplev3@hotmail.com",
  "groups": [
    "20bc64d1-fc89-40bb-871e-47602508d99b",
    "096af11e-ca54-4eb6-8a78-0903fef7048f"
  ]
}
```

---

# RBAC Implementation

## Admin Access

Admin page requires membership in:

```text
IAM-Admins
```

Application validates:

```python
if IAM_ADMINS_GROUP_ID in groups:
    allow_access()
else:
    deny_access()
```

---

# UI Improvements

Implemented:

* Enterprise-style navigation bar
* Dashboard page
* Admin page
* Access denied page
* Responsive CSS styling
* Group badges
* User information cards

Static assets:

```text
/static/css/style.css
```

---

# Lessons Learned

* Difference between OIDC and SAML
* Microsoft Entra App Registrations
* Token Configuration
* Group Claims
* Optional Claims
* OAuth Authorization Code Flow
* Flask Session Management
* RBAC Authorization Logic
* Enterprise IAM Concepts

---

# Future Enhancements

## Phase 2

* Microsoft Graph API Integration
* Resolve Group IDs to Group Names
* Audit Logging
* User Administration Page
* Access Review Dashboard
* Joiner-Mover-Leaver Workflow

## Phase 3

* MFA Reporting
* Conditional Access Visualization
* Identity Governance Dashboard
* Automated User Provisioning

---

# Skills Demonstrated

* Identity and Access Management (IAM)
* Microsoft Entra ID
* OpenID Connect (OIDC)
* OAuth 2.0
* RBAC
* JWT Tokens
* Flask Development
* Python Development
* Microsoft Graph
* Security Engineering
* Authentication and Authorization
* Enterprise Identity Management
* Azure Administration

```
```
