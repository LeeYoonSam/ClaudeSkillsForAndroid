package com.example.shopping.data.repository

import com.example.shopping.data.remote.ProductCatalogApi
import com.example.shopping.data.remote.toDomain
import com.example.shopping.domain.model.ProductCatalog
import com.example.shopping.domain.repository.ProductCatalogRepository
import javax.inject.Inject

// SPEC-002: Repository implementation
class ProductCatalogRepositoryImpl @Inject constructor(
    private val api: ProductCatalogApi,
) : ProductCatalogRepository {

    override suspend fun getProductCatalog(id: String): Result<ProductCatalog> {
        return try {
            val response = api.getProductCatalog(id)
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
