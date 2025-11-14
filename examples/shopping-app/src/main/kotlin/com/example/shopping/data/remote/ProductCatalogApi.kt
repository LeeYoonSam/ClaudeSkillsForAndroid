package com.example.shopping.data.remote

import com.example.shopping.data.remote.ProductCatalogDto
import retrofit2.Response
import retrofit2.http.GET
import retrofit2.http.Path

// SPEC-002: API interface
interface ProductCatalogApi {
    @GET("api/productcatalog/{id}")
    suspend fun getProductCatalog(@Path("id") id: String): Response<ProductCatalogDto>
}
