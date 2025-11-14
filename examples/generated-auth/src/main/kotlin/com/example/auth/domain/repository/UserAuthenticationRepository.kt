package com.example.auth.domain.repository

import com.example.auth.domain.model.UserAuthentication

// SPEC-001: Repository interface
interface UserAuthenticationRepository {
    suspend fun getUserAuthentication(id: String): Result<UserAuthentication>
    // TODO: Add methods based on SPEC requirements
}
