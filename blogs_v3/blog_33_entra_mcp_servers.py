"""
Blog Post 33: Entra Authentication for MCP Servers
"""

BLOG_POST = {
    "title": "Using On-Behalf-Of Flow for Entra-Based MCP Servers: Secure Agent-to-Service Authentication",
    
    "coverImage": "https://static.wixstatic.com/media/32fce1_6c1cc8bc82db46b998b61dc5273d7d99~mv2.png",
    
    "content": """The Model Context Protocol (MCP) has emerged as the standard for connecting AI agents to external tools and services. But connecting agents to enterprise services raises critical authentication questions: How do agents authenticate to backend services? How do permissions flow from users through agents to the services they access? Microsoft Entra's on-behalf-of flow provides the answer.

The authentication challenge for MCP servers is nuanced. When a user interacts with an agent, and that agent needs to access enterprise services, the service needs to know who the original user is. Simple API keys don't capture user identity. Shared credentials create security risks. The authentication model needs to propagate identity through the agent layer.

On-behalf-of (OBO) flow solves this problem elegantly. The user authenticates to the application. The application obtains a token for the user. When the application (or agent) needs to call a downstream service, it exchanges the user's token for a new token valid for that service. The downstream service sees the original user's identity and can enforce appropriate permissions.

Implementing OBO for MCP servers requires understanding the token exchange mechanics. The MCP server receives a token from the agent. It validates this token against Entra. It then requests a new token for the backend service, passing the original token as assertion. Entra validates the chain and issues a new token if the user has appropriate permissions.

The permission model provides granular control. Administrators configure which applications can request OBO tokens for which services. Users consent to the permissions applications can exercise on their behalf. The security boundary is maintained—agents can only access what users could access directly.

Python implementation patterns demonstrate the practical approach. Using the MSAL library, MCP servers can handle the token exchange with relatively little code. The complexity is in understanding the flow, not in implementation. Once the pattern is clear, adding OBO to MCP servers is straightforward.

Error handling requires attention to the various failure modes. Token expiration, permission denial, and service unavailability all need appropriate handling. The MCP server should provide useful error messages that help debug authentication issues without leaking security-sensitive information.

Token caching improves performance and reduces Entra load. Tokens have limited lifetime but can be reused within that window. Proper caching avoids unnecessary token requests while respecting token lifetime. The balance between performance and security needs careful consideration.

Refresh token handling enables long-running agent sessions. When access tokens expire, refresh tokens can obtain new access tokens without requiring user re-authentication. MCP servers that support extended sessions need refresh token logic. The user experience improves when authentication doesn't interrupt workflows.

Multi-tenant scenarios add complexity but are fully supported. MCP servers can authenticate users from multiple Entra tenants. The application registration configures which tenants are acceptable. Enterprise deployments often require multi-tenant support for partner access or multi-organization scenarios.

Monitoring and logging provide visibility into authentication flows. Successful and failed authentication attempts should be logged for security analysis. Anomalous patterns might indicate attacks. The logging needs to capture enough detail for investigation without storing sensitive token content.

Testing the authentication flow requires appropriate test infrastructure. Test tenants, test users, and test applications enable validation without affecting production. Automated testing should verify both success and failure scenarios. The authentication layer is too critical for manual-only testing.

For organizations building MCP servers that access enterprise resources, Entra OBO provides the authentication foundation. The identity flows properly from user through agent to service. Permissions are enforced at each layer. The enterprise security model extends to the agent era.

---

*Stay radical, stay curious, and keep pushing the boundaries of what's possible in the cloud.*

**Chriz**
*Beyond Cloud with Chriz*""",
    
    "excerpt": "Microsoft Entra's on-behalf-of flow enables secure authentication for MCP servers, propagating user identity through AI agents to backend services while maintaining enterprise permission enforcement.",
    
    "publish": True,
    
    "tags": ["Azure", "Microsoft Entra", "MCP", "Authentication", "Security", "AI Agents"]
}
