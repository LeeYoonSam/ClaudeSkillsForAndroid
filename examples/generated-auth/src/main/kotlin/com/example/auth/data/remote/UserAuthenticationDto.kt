package com.example.auth.data.remote

import com.example.auth.domain.model.UserAuthentication
import kotlinx.serialization.Serializable

// SPEC-001: Data transfer object
@Serializable
data class UserAuthenticationDto(
    val id: String,
    // TODO: Add fields based on SPEC
)

// SPEC-001: Mapper from DTO to Domain
fun UserAuthenticationDto.toDomain(): UserAuthentication = UserAuthentication(
    id = id,
    // TODO: Map fields
)
