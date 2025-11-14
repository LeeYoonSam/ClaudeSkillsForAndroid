package com.example.auth.domain.usecase

import com.example.auth.domain.model.UserAuthentication
import com.example.auth.domain.repository.UserAuthenticationRepository
import javax.inject.Inject

// SPEC-001: Get UserAuthentication use case
class GetUserAuthenticationUseCase @Inject constructor(
    private val repository: UserAuthenticationRepository
) {
    suspend operator fun invoke(id: String): Result<UserAuthentication> {
        return repository.getUserAuthentication(id)
    }
}
