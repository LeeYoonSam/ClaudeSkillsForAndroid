package com.example.auth.domain

import com.example.auth.domain.model.UserAuthentication
import com.example.auth.domain.repository.UserAuthenticationRepository
import com.example.auth.domain.usecase.GetUserAuthenticationUseCase
import kotlinx.coroutines.test.runTest
import org.junit.Before
import org.junit.Test
import org.mockito.Mock
import org.mockito.Mockito.`when`
import org.mockito.MockitoAnnotations
import kotlin.test.assertTrue

// TEST-SPEC-001-U-01: Test GetUserAuthenticationUseCase
class UserAuthenticationUseCaseTest {

    @Mock
    private lateinit var repository: UserAuthenticationRepository

    private lateinit var useCase: GetUserAuthenticationUseCase

    @Before
    fun setup() {
        MockitoAnnotations.openMocks(this)
        useCase = GetUserAuthenticationUseCase(repository)
    }

    @Test
    fun `get userauthentication returns success`() = runTest {
        // Given
        val id = "test-id"
        val expectedUserAuthentication = UserAuthentication(id = id)
        `when`(repository.getUserAuthentication(id)).thenReturn(Result.success(expectedUserAuthentication))

        // When
        val result = useCase(id)

        // Then
        assertTrue(result.isSuccess)
    }
}
