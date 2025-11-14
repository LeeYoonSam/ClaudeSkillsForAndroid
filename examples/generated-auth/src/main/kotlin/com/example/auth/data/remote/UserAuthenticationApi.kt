package com.example.auth.data.remote

import com.example.auth.data.remote.UserAuthenticationDto
import retrofit2.Response
import retrofit2.http.GET
import retrofit2.http.Path

// SPEC-001: API interface
interface UserAuthenticationApi {
    @GET("api/userauthentication/{id}")
    suspend fun getUserAuthentication(@Path("id") id: String): Response<UserAuthenticationDto>
}
