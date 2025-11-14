package com.example.auth.data.repository

import com.example.auth.data.remote.UserAuthenticationApi
import com.example.auth.data.remote.toDomain
import com.example.auth.domain.model.UserAuthentication
import com.example.auth.domain.repository.UserAuthenticationRepository
import javax.inject.Inject

// SPEC-001: Repository implementation
class UserAuthenticationRepositoryImpl @Inject constructor(
    private val api: UserAuthenticationApi,
) : UserAuthenticationRepository {

    override suspend fun getUserAuthentication(id: String): Result<UserAuthentication> {
        return try {
            val response = api.getUserAuthentication(id)
            if (response.isSuccessful) {
                response.body()?.let {
                    Result.success(it.toDomain())
                } ?: Result.failure(Exception("Empty response"))
            } else {
                Result.failure(Exception("Error: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
