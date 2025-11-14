---
spec_id: API-XXX
api_name: [API Name]
version: 1.0.0
author: [Author Name]
date: [YYYY-MM-DD]
base_url: https://api.example.com/v1
status: draft
traceability:
  parent_spec: SPEC-XXX
  requirements: [REQ-XXX, REQ-YYY]
---

# [API Name] API Specification

## 1. Overview

**Purpose**: [Brief description of what this API does]

**Version**: 1.0.0

**Base URL**: `https://api.example.com/v1`

**Authentication**: [Bearer Token / API Key / OAuth2]

**Rate Limiting**: [X requests per minute]

---

## 2. Authentication

### 2.1 Authentication Method

**Type**: Bearer Token

**Header**:
```http
Authorization: Bearer {access_token}
```

**Example**:
```http
GET /api/users HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 2.2 Authentication Errors

| Status Code | Error Code | Description |
|-------------|------------|-------------|
| 401 | `unauthorized` | Missing or invalid token |
| 403 | `forbidden` | Valid token but insufficient permissions |

---

## 3. API Endpoints

### 3.1 List [Resources]

**Endpoint**: `GET /api/[resources]`

**Description**: Retrieves a list of [resources] with pagination

**Requirements**: REQ-XXX-U-01

**Request**:
```http
GET /api/[resources]?page=1&limit=20&sort=created_at&order=desc HTTP/1.1
Host: api.example.com
Authorization: Bearer {token}
```

**Query Parameters**:
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `page` | Integer | No | 1 | Page number (1-indexed) |
| `limit` | Integer | No | 20 | Items per page (max: 100) |
| `sort` | String | No | `created_at` | Field to sort by |
| `order` | String | No | `desc` | Sort order (`asc` or `desc`) |
| `search` | String | No | - | Search query |

**Response** (200 OK):
```json
{
  "data": [
    {
      "id": "uuid-here",
      "name": "Resource Name",
      "description": "Description",
      "created_at": "2025-11-14T09:00:00Z",
      "updated_at": "2025-11-14T09:00:00Z"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "total_items": 100,
    "items_per_page": 20
  }
}
```

**Error Responses**:
| Status Code | Error Code | Description | Example |
|-------------|------------|-------------|---------|
| 400 | `invalid_parameter` | Invalid query parameter | `{"error": "invalid_parameter", "message": "limit must be between 1 and 100"}` |
| 401 | `unauthorized` | Missing authentication | `{"error": "unauthorized", "message": "Authentication required"}` |
| 500 | `internal_error` | Server error | `{"error": "internal_error", "message": "Internal server error"}` |

---

### 3.2 Get [Resource] by ID

**Endpoint**: `GET /api/[resources]/{id}`

**Description**: Retrieves a single [resource] by ID

**Requirements**: REQ-XXX-U-02

**Request**:
```http
GET /api/[resources]/123e4567-e89b-12d3-a456-426614174000 HTTP/1.1
Host: api.example.com
Authorization: Bearer {token}
```

**Path Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | UUID | Yes | Resource unique identifier |

**Response** (200 OK):
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Resource Name",
  "description": "Detailed description",
  "status": "active",
  "metadata": {
    "key1": "value1",
    "key2": "value2"
  },
  "created_at": "2025-11-14T09:00:00Z",
  "updated_at": "2025-11-14T09:00:00Z"
}
```

**Error Responses**:
| Status Code | Error Code | Description |
|-------------|------------|-------------|
| 404 | `not_found` | Resource not found |
| 401 | `unauthorized` | Missing authentication |

---

### 3.3 Create [Resource]

**Endpoint**: `POST /api/[resources]`

**Description**: Creates a new [resource]

**Requirements**: REQ-XXX-U-03

**Request**:
```http
POST /api/[resources] HTTP/1.1
Host: api.example.com
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "New Resource",
  "description": "Description",
  "metadata": {
    "key": "value"
  }
}
```

**Request Body**:
| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| `name` | String | Yes | 1-100 chars | Resource name |
| `description` | String | No | Max 500 chars | Description |
| `metadata` | Object | No | - | Additional metadata |

**Response** (201 Created):
```json
{
  "id": "new-uuid-here",
  "name": "New Resource",
  "description": "Description",
  "status": "active",
  "metadata": {
    "key": "value"
  },
  "created_at": "2025-11-14T09:00:00Z",
  "updated_at": "2025-11-14T09:00:00Z"
}
```

**Error Responses**:
| Status Code | Error Code | Description | Example |
|-------------|------------|-------------|---------|
| 400 | `validation_error` | Invalid request body | `{"error": "validation_error", "fields": {"name": "Name is required"}}` |
| 409 | `conflict` | Resource already exists | `{"error": "conflict", "message": "Resource with this name already exists"}` |

---

### 3.4 Update [Resource]

**Endpoint**: `PUT /api/[resources]/{id}`

**Description**: Updates an existing [resource]

**Requirements**: REQ-XXX-U-04

**Request**:
```http
PUT /api/[resources]/123e4567-e89b-12d3-a456-426614174000 HTTP/1.1
Host: api.example.com
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Updated Name",
  "description": "Updated description"
}
```

**Request Body**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | String | No | Updated name |
| `description` | String | No | Updated description |
| `metadata` | Object | No | Updated metadata |

**Response** (200 OK):
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Updated Name",
  "description": "Updated description",
  "status": "active",
  "created_at": "2025-11-14T09:00:00Z",
  "updated_at": "2025-11-14T10:00:00Z"
}
```

**Error Responses**:
| Status Code | Error Code | Description |
|-------------|------------|-------------|
| 404 | `not_found` | Resource not found |
| 400 | `validation_error` | Invalid request body |

---

### 3.5 Delete [Resource]

**Endpoint**: `DELETE /api/[resources]/{id}`

**Description**: Deletes a [resource]

**Requirements**: REQ-XXX-U-05

**Request**:
```http
DELETE /api/[resources]/123e4567-e89b-12d3-a456-426614174000 HTTP/1.1
Host: api.example.com
Authorization: Bearer {token}
```

**Response** (204 No Content):
```
(Empty response body)
```

**Error Responses**:
| Status Code | Error Code | Description |
|-------------|------------|-------------|
| 404 | `not_found` | Resource not found |
| 409 | `conflict` | Cannot delete (has dependencies) |

---

## 4. Data Models

### 4.1 [Resource] Object

```typescript
interface Resource {
  id: string;              // UUID
  name: string;            // 1-100 characters
  description?: string;    // Optional, max 500 characters
  status: 'active' | 'inactive' | 'archived';
  metadata?: Record<string, any>;
  created_at: string;      // ISO 8601 datetime
  updated_at: string;      // ISO 8601 datetime
}
```

### 4.2 Pagination Object

```typescript
interface Pagination {
  current_page: number;
  total_pages: number;
  total_items: number;
  items_per_page: number;
}
```

### 4.3 Error Response Object

```typescript
interface ErrorResponse {
  error: string;           // Error code
  message: string;         // Human-readable message
  fields?: Record<string, string>; // Field-specific errors
  trace_id?: string;       // Request trace ID
}
```

---

## 5. Retrofit Implementation (Kotlin)

### 5.1 API Service Interface

```kotlin
// API-XXX: [API Name] service interface
interface [Resource]Api {

    // API-XXX: List resources (REQ-XXX-U-01)
    @GET("api/[resources]")
    suspend fun get[Resources](
        @Query("page") page: Int = 1,
        @Query("limit") limit: Int = 20,
        @Query("sort") sort: String = "created_at",
        @Query("order") order: String = "desc",
        @Query("search") search: String? = null,
    ): Response<[Resource]ListResponse>

    // API-XXX: Get resource by ID (REQ-XXX-U-02)
    @GET("api/[resources]/{id}")
    suspend fun get[Resource](
        @Path("id") id: String,
    ): Response<[Resource]Dto>

    // API-XXX: Create resource (REQ-XXX-U-03)
    @POST("api/[resources]")
    suspend fun create[Resource](
        @Body request: Create[Resource]Request,
    ): Response<[Resource]Dto>

    // API-XXX: Update resource (REQ-XXX-U-04)
    @PUT("api/[resources]/{id}")
    suspend fun update[Resource](
        @Path("id") id: String,
        @Body request: Update[Resource]Request,
    ): Response<[Resource]Dto>

    // API-XXX: Delete resource (REQ-XXX-U-05)
    @DELETE("api/[resources]/{id}")
    suspend fun delete[Resource](
        @Path("id") id: String,
    ): Response<Unit>
}
```

### 5.2 Data Transfer Objects (DTOs)

```kotlin
// API-XXX: Response DTO
@Serializable
data class [Resource]Dto(
    val id: String,
    val name: String,
    val description: String? = null,
    val status: String,
    val metadata: Map<String, JsonElement>? = null,
    @SerialName("created_at") val createdAt: String,
    @SerialName("updated_at") val updatedAt: String,
)

// API-XXX: List response
@Serializable
data class [Resource]ListResponse(
    val data: List<[Resource]Dto>,
    val pagination: PaginationDto,
)

@Serializable
data class PaginationDto(
    @SerialName("current_page") val currentPage: Int,
    @SerialName("total_pages") val totalPages: Int,
    @SerialName("total_items") val totalItems: Int,
    @SerialName("items_per_page") val itemsPerPage: Int,
)

// API-XXX: Create request
@Serializable
data class Create[Resource]Request(
    val name: String,
    val description: String? = null,
    val metadata: Map<String, JsonElement>? = null,
)

// API-XXX: Update request
@Serializable
data class Update[Resource]Request(
    val name: String? = null,
    val description: String? = null,
    val metadata: Map<String, JsonElement>? = null,
)

// API-XXX: Error response
@Serializable
data class ApiErrorResponse(
    val error: String,
    val message: String,
    val fields: Map<String, String>? = null,
    @SerialName("trace_id") val traceId: String? = null,
)
```

### 5.3 Domain Mappers

```kotlin
// API-XXX: Mapper from DTO to Domain
fun [Resource]Dto.toDomain(): [Resource] = [Resource](
    id = id,
    name = name,
    description = description,
    status = [Resource]Status.valueOf(status.uppercase()),
    createdAt = Instant.parse(createdAt),
    updatedAt = Instant.parse(updatedAt),
)

// API-XXX: Mapper from Domain to DTO
fun [Resource].toDto(): [Resource]Dto = [Resource]Dto(
    id = id,
    name = name,
    description = description,
    status = status.name.lowercase(),
    createdAt = createdAt.toString(),
    updatedAt = updatedAt.toString(),
)
```

---

## 6. Error Handling

### 6.1 HTTP Status Codes

| Status Code | Meaning | Usage |
|-------------|---------|-------|
| 200 | OK | Successful GET, PUT |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid request body or parameters |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Resource conflict (e.g., duplicate) |
| 422 | Unprocessable Entity | Validation errors |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Service temporarily down |

### 6.2 Error Response Format

All errors follow this format:
```json
{
  "error": "error_code",
  "message": "Human-readable error message",
  "fields": {
    "field_name": "Field-specific error message"
  },
  "trace_id": "unique-trace-id"
}
```

### 6.3 Kotlin Error Handling

```kotlin
// API-XXX: Handle API errors
suspend fun <T> safeApiCall(
    apiCall: suspend () -> Response<T>
): Result<T> {
    return try {
        val response = apiCall()
        when {
            response.isSuccessful -> {
                response.body()?.let { Result.success(it) }
                    ?: Result.failure(Exception("Empty response body"))
            }
            response.code() == 401 -> {
                Result.failure(UnauthorizedException())
            }
            response.code() == 404 -> {
                Result.failure(NotFoundException())
            }
            else -> {
                val errorBody = response.errorBody()?.string()
                val error = parseError(errorBody)
                Result.failure(ApiException(error))
            }
        }
    } catch (e: IOException) {
        Result.failure(NetworkException(e))
    } catch (e: Exception) {
        Result.failure(e)
    }
}
```

---

## 7. Rate Limiting

**Limit**: 100 requests per minute per API key

**Headers**:
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1699876800
```

**Rate Limit Exceeded Response** (429):
```json
{
  "error": "rate_limit_exceeded",
  "message": "Rate limit exceeded. Try again in 60 seconds.",
  "retry_after": 60
}
```

---

## 8. Versioning

**Strategy**: URL-based versioning

**Current Version**: `v1`

**Example**:
- v1: `https://api.example.com/v1/resources`
- v2 (future): `https://api.example.com/v2/resources`

**Deprecation Policy**: Old versions supported for 6 months after new version release

---

## 9. Testing

### 9.1 Mock API Responses

```kotlin
// TEST-API-XXX-01: Mock successful list response
val mockListResponse = [Resource]ListResponse(
    data = listOf(
        [Resource]Dto(
            id = "test-id-1",
            name = "Test Resource 1",
            status = "active",
            createdAt = "2025-11-14T09:00:00Z",
            updatedAt = "2025-11-14T09:00:00Z",
        )
    ),
    pagination = PaginationDto(
        currentPage = 1,
        totalPages = 1,
        totalItems = 1,
        itemsPerPage = 20,
    )
)
```

### 9.2 Integration Test Example

```kotlin
@Test
fun `test get resource by id returns 200`() = runTest {
    // Given
    val resourceId = "test-id"
    mockWebServer.enqueue(
        MockResponse()
            .setResponseCode(200)
            .setBody(mockResourceJson)
    )

    // When
    val result = api.get[Resource](resourceId)

    // Then
    assertTrue(result.isSuccessful)
    assertEquals("Test Resource", result.body()?.name)
}
```

---

## 10. Changelog

### v1.0.0 (2025-11-14)
- Initial API specification
- Added CRUD endpoints for [Resource]
- Implemented pagination
- Added authentication

---

## 11. Related Documentation

- **Parent SPEC**: SPEC-XXX
- **Related Skills**: `android-networking-retrofit`, `android-coroutines`
- **External API Docs**: [Link]

---

## 12. Notes

**Security Considerations**:
- All endpoints require authentication
- Sensitive data is not logged
- HTTPS only (TLS 1.2+)

**Performance**:
- Response time SLA: < 500ms (p95)
- Pagination recommended for large datasets
- Caching headers provided

**Future Enhancements**:
- WebSocket support for real-time updates
- Batch operations endpoint
- Advanced filtering options
