# LocalFix 🔧

### Smart Local Service Management Platform

LocalFix is a full-stack web application that connects customers with local service providers such as plumbers, electricians, mechanics, AC technicians, and other professionals.

Customers can browse available services, select a verified provider, submit service requests, track request status, cancel pending requests, and provide ratings and reviews after service completion.

Service providers can create their professional profile, select the services they provide, view customer requests, and manage requests through different stages.

Administrators can verify service providers and manage provider verification.

---

## 🚀 Features

### 👤 Customer

- Customer registration and login
- JWT-based authentication
- Browse available services
- View service details and base prices
- View verified providers for a selected service
- Select a service provider
- Submit service requests
- View personal service requests
- Track service request status
- Cancel pending requests
- Submit ratings and reviews for completed services
- Logout

### 🧑‍🔧 Service Provider

- Provider registration and login
- Create and update professional profile
- Add phone number and address
- Add years of experience
- Select multiple services offered
- View customer service requests
- Accept service requests
- Reject service requests
- Start accepted requests
- Mark services as completed
- Logout

### 👨‍💼 Administrator

- Admin authentication
- View registered service providers
- View total providers
- View verified providers
- View pending providers
- Verify service providers

### 🔐 Authentication & Security

- JWT authentication
- Access and refresh tokens
- Role-based authorization
- Angular route guards
- HTTP authentication interceptor
- Backend permission classes
- Protected API endpoints

---

## 🔄 Service Request Workflow

A service request follows a controlled status flow:

```text
PENDING
   │
   ├── ACCEPTED
   │      │
   │      └── IN_PROGRESS
   │              │
   │              └── COMPLETED
   │
   └── REJECTED