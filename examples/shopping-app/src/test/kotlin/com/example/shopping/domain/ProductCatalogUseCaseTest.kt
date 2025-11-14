package com.example.shopping.domain

import com.example.shopping.domain.model.ProductCatalog
import com.example.shopping.domain.repository.ProductCatalogRepository
import com.example.shopping.domain.usecase.GetProductCatalogUseCase
import kotlinx.coroutines.test.runTest
import org.junit.Before
import org.junit.Test
import org.mockito.Mock
import org.mockito.Mockito.`when`
import org.mockito.MockitoAnnotations
import kotlin.test.assertTrue

// TEST-SPEC-002-U-01: Test GetProductCatalogUseCase
class ProductCatalogUseCaseTest {

    @Mock
    private lateinit var repository: ProductCatalogRepository

    private lateinit var useCase: GetProductCatalogUseCase

    @Before
    fun setup() {
        MockitoAnnotations.openMocks(this)
        useCase = GetProductCatalogUseCase(repository)
    }

    @Test
    fun `get productcatalog returns success`() = runTest {
        // Given
        val id = "test-id"
        val expectedProductCatalog = ProductCatalog(id = id)
        `when`(repository.getProductCatalog(id)).thenReturn(Result.success(expectedProductCatalog))

        // When
        val result = useCase(id)

        // Then
        assertTrue(result.isSuccess)
    }
}
