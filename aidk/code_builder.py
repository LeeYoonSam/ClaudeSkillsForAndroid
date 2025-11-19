#!/usr/bin/env python3
"""
Code Builder Agent

Generates Android code from SPEC documents following Clean Architecture.
Automatically loads related skills and generates domain, data, and presentation layers.

Usage:
    python code_builder.py generate specs/examples/user-authentication/SPEC.md
    python code_builder.py generate specs/examples/user-authentication/SPEC.md --output ./output
"""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


@dataclass
class Requirement:
    """Represents a single requirement."""
    id: str
    type: str  # U, S, E, O, N
    description: str


@dataclass
class SpecDocument:
    """Parsed SPEC document."""
    spec_id: str
    feature: str
    status: str
    version: str
    author: str
    date: str
    related_skills: List[str]
    requirements: List[Requirement]
    purpose: str


class SpecParser:
    """Parses SPEC.md files."""

    @staticmethod
    def parse(spec_file: Path) -> SpecDocument:
        """Parse a SPEC.md file.

        Args:
            spec_file: Path to SPEC.md

        Returns:
            Parsed SpecDocument
        """
        with open(spec_file, 'r') as f:
            content = f.read()

        # Parse frontmatter
        frontmatter_match = re.search(r'---\n(.*?)\n---', content, re.DOTALL)
        if not frontmatter_match:
            raise ValueError("No frontmatter found in SPEC file")

        frontmatter = frontmatter_match.group(1)

        # Extract metadata
        spec_id = SpecParser._extract_field(frontmatter, 'spec_id')
        feature = SpecParser._extract_field(frontmatter, 'feature')
        status = SpecParser._extract_field(frontmatter, 'status', 'draft')
        version = SpecParser._extract_field(frontmatter, 'version', '1.0.0')
        author = SpecParser._extract_field(frontmatter, 'author', 'Unknown')
        date = SpecParser._extract_field(frontmatter, 'date', '')

        # Extract related skills
        skills_match = re.search(r'related_skills:\n((?:  - .*\n)*)', frontmatter)
        related_skills = []
        if skills_match:
            skills_text = skills_match.group(1)
            related_skills = [
                line.strip().replace('- ', '')
                for line in skills_text.split('\n')
                if line.strip().startswith('-')
            ]

        # Extract purpose
        purpose_match = re.search(r'\*\*Purpose\*\*: (.+)', content)
        purpose = purpose_match.group(1) if purpose_match else ""

        # Extract requirements
        requirements = SpecParser._extract_requirements(content)

        return SpecDocument(
            spec_id=spec_id,
            feature=feature,
            status=status,
            version=version,
            author=author,
            date=date,
            related_skills=related_skills,
            requirements=requirements,
            purpose=purpose
        )

    @staticmethod
    def _extract_field(text: str, field: str, default: str = '') -> str:
        """Extract a field from frontmatter."""
        match = re.search(rf'{field}:\s*(.+)', text)
        return match.group(1).strip() if match else default

    @staticmethod
    def _extract_requirements(content: str) -> List[Requirement]:
        """Extract requirements from SPEC content."""
        requirements = []

        # Pattern: - **REQ-XXX-Y-ZZ**: Description
        pattern = r'-\s+\*\*([A-Z-]+)\*\*:\s+(.+)'
        matches = re.finditer(pattern, content)

        for match in matches:
            req_id = match.group(1)
            description = match.group(2).strip()

            # Determine type from ID (REQ-001-U-01 -> U)
            type_match = re.search(r'-([USEON])-', req_id)
            req_type = type_match.group(1) if type_match else 'U'

            requirements.append(Requirement(
                id=req_id,
                type=req_type,
                description=description
            ))

        return requirements


class CodeGenerator:
    """Generates Android code from SPEC."""

    def __init__(self, spec: SpecDocument, output_dir: Path):
        """Initialize code generator.

        Args:
            spec: Parsed SPEC document
            output_dir: Output directory for generated code
        """
        self.spec = spec
        self.output_dir = output_dir
        self.package_name = "com.example.app"  # Default package
        self.feature_name = spec.feature.replace(" ", "").replace("-", "")

    def generate_all(self):
        """Generate all code layers."""
        print(f"\n{Colors.HEADER}{Colors.BOLD}=== Code Builder ==={Colors.ENDC}\n")
        print(f"{Colors.OKBLUE}Generating code for: {self.spec.feature} (SPEC-{self.spec.spec_id}){Colors.ENDC}")
        print(f"{Colors.OKBLUE}Related Skills: {len(self.spec.related_skills)}{Colors.ENDC}\n")

        self._create_directory_structure()
        self.generate_domain_layer()
        self.generate_data_layer()
        self.generate_presentation_layer()
        self.generate_tests()

        print(f"\n{Colors.OKGREEN}{Colors.BOLD}✓ Code generation complete!{Colors.ENDC}")
        print(f"{Colors.OKBLUE}Output: {self.output_dir}{Colors.ENDC}")

    def _create_directory_structure(self):
        """Create Clean Architecture directory structure."""
        base_path = self.output_dir / "src" / "main" / "kotlin" / self.package_name.replace(".", "/")
        test_path = self.output_dir / "src" / "test" / "kotlin" / self.package_name.replace(".", "/")

        # Main source directories
        (base_path / "domain" / "model").mkdir(parents=True, exist_ok=True)
        (base_path / "domain" / "usecase").mkdir(parents=True, exist_ok=True)
        (base_path / "domain" / "repository").mkdir(parents=True, exist_ok=True)

        (base_path / "data" / "remote").mkdir(parents=True, exist_ok=True)
        (base_path / "data" / "local").mkdir(parents=True, exist_ok=True)
        (base_path / "data" / "repository").mkdir(parents=True, exist_ok=True)

        (base_path / "presentation" / "viewmodel").mkdir(parents=True, exist_ok=True)
        (base_path / "presentation" / "ui").mkdir(parents=True, exist_ok=True)
        (base_path / "presentation" / "state").mkdir(parents=True, exist_ok=True)

        # Test directories
        (test_path / "domain").mkdir(parents=True, exist_ok=True)
        (test_path / "data").mkdir(parents=True, exist_ok=True)
        (test_path / "presentation").mkdir(parents=True, exist_ok=True)

    def generate_domain_layer(self):
        """Generate domain layer code."""
        print(f"{Colors.OKCYAN}Generating Domain Layer...{Colors.ENDC}")

        # Generate model
        model_code = self._generate_domain_model()
        self._write_file("domain/model", f"{self.feature_name}.kt", model_code)

        # Generate repository interface
        repo_interface = self._generate_repository_interface()
        self._write_file("domain/repository", f"{self.feature_name}Repository.kt", repo_interface)

        # Generate use cases
        usecases = self._generate_usecases()
        for usecase_name, usecase_code in usecases:
            self._write_file("domain/usecase", f"{usecase_name}.kt", usecase_code)

        print(f"  {Colors.OKGREEN}✓ Domain layer complete{Colors.ENDC}")

    def generate_data_layer(self):
        """Generate data layer code."""
        print(f"{Colors.OKCYAN}Generating Data Layer...{Colors.ENDC}")

        # Generate API interface
        api_code = self._generate_api_interface()
        self._write_file("data/remote", f"{self.feature_name}Api.kt", api_code)

        # Generate DTOs
        dto_code = self._generate_dtos()
        self._write_file("data/remote", f"{self.feature_name}Dto.kt", dto_code)

        # Generate repository implementation
        repo_impl = self._generate_repository_implementation()
        self._write_file("data/repository", f"{self.feature_name}RepositoryImpl.kt", repo_impl)

        print(f"  {Colors.OKGREEN}✓ Data layer complete{Colors.ENDC}")

    def generate_presentation_layer(self):
        """Generate presentation layer code."""
        print(f"{Colors.OKCYAN}Generating Presentation Layer...{Colors.ENDC}")

        # Generate state
        state_code = self._generate_state()
        self._write_file("presentation/state", f"{self.feature_name}State.kt", state_code)

        # Generate ViewModel
        viewmodel_code = self._generate_viewmodel()
        self._write_file("presentation/viewmodel", f"{self.feature_name}ViewModel.kt", viewmodel_code)

        # Generate Screen
        screen_code = self._generate_screen()
        self._write_file("presentation/ui", f"{self.feature_name}Screen.kt", screen_code)

        print(f"  {Colors.OKGREEN}✓ Presentation layer complete{Colors.ENDC}")

    def generate_tests(self):
        """Generate test files."""
        print(f"{Colors.OKCYAN}Generating Tests...{Colors.ENDC}")

        # Generate unit tests
        test_code = self._generate_unit_tests()
        test_path = self.output_dir / "src" / "test" / "kotlin" / self.package_name.replace(".", "/") / "domain"
        test_file = test_path / f"{self.feature_name}UseCaseTest.kt"
        test_file.parent.mkdir(parents=True, exist_ok=True)
        test_file.write_text(test_code)

        print(f"  {Colors.OKGREEN}✓ Tests complete{Colors.ENDC}")

    def _write_file(self, subdir: str, filename: str, content: str):
        """Write generated code to file."""
        base_path = self.output_dir / "src" / "main" / "kotlin" / self.package_name.replace(".", "/")
        file_path = base_path / subdir / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)

    def _generate_domain_model(self) -> str:
        """Generate domain model."""
        return f"""package {self.package_name}.domain.model

// {self.spec.spec_id}: {self.spec.feature}
// Purpose: {self.spec.purpose}
data class {self.feature_name}(
    val id: String,
    // TODO: Add properties based on SPEC requirements
)
"""

    def _generate_repository_interface(self) -> str:
        """Generate repository interface."""
        return f"""package {self.package_name}.domain.repository

import {self.package_name}.domain.model.{self.feature_name}

// {self.spec.spec_id}: Repository interface
interface {self.feature_name}Repository {{
    suspend fun get{self.feature_name}(id: String): Result<{self.feature_name}>
    // TODO: Add methods based on SPEC requirements
}}
"""

    def _generate_usecases(self) -> List[Tuple[str, str]]:
        """Generate use cases."""
        usecases = []

        usecase_name = f"Get{self.feature_name}UseCase"
        usecase_code = f"""package {self.package_name}.domain.usecase

import {self.package_name}.domain.model.{self.feature_name}
import {self.package_name}.domain.repository.{self.feature_name}Repository
import javax.inject.Inject

// {self.spec.spec_id}: Get {self.feature_name} use case
class {usecase_name} @Inject constructor(
    private val repository: {self.feature_name}Repository
) {{
    suspend operator fun invoke(id: String): Result<{self.feature_name}> {{
        return repository.get{self.feature_name}(id)
    }}
}}
"""
        usecases.append((usecase_name, usecase_code))

        return usecases

    def _generate_api_interface(self) -> str:
        """Generate API interface."""
        return f"""package {self.package_name}.data.remote

import {self.package_name}.data.remote.{self.feature_name}Dto
import retrofit2.Response
import retrofit2.http.GET
import retrofit2.http.Path

// {self.spec.spec_id}: API interface
interface {self.feature_name}Api {{
    @GET("api/{self.feature_name.lower()}/{{id}}")
    suspend fun get{self.feature_name}(@Path("id") id: String): Response<{self.feature_name}Dto>
}}
"""

    def _generate_dtos(self) -> str:
        """Generate DTOs."""
        return f"""package {self.package_name}.data.remote

import {self.package_name}.domain.model.{self.feature_name}
import kotlinx.serialization.Serializable

// {self.spec.spec_id}: Data transfer object
@Serializable
data class {self.feature_name}Dto(
    val id: String,
    // TODO: Add fields based on SPEC
)

// {self.spec.spec_id}: Mapper from DTO to Domain
fun {self.feature_name}Dto.toDomain(): {self.feature_name} = {self.feature_name}(
    id = id,
    // TODO: Map fields
)
"""

    def _generate_repository_implementation(self) -> str:
        """Generate repository implementation."""
        return f"""package {self.package_name}.data.repository

import {self.package_name}.data.remote.{self.feature_name}Api
import {self.package_name}.data.remote.toDomain
import {self.package_name}.domain.model.{self.feature_name}
import {self.package_name}.domain.repository.{self.feature_name}Repository
import javax.inject.Inject

// {self.spec.spec_id}: Repository implementation
class {self.feature_name}RepositoryImpl @Inject constructor(
    private val api: {self.feature_name}Api,
) : {self.feature_name}Repository {{

    override suspend fun get{self.feature_name}(id: String): Result<{self.feature_name}> {{
        return try {{
            val response = api.get{self.feature_name}(id)
            if (response.isSuccessful) {{
                response.body()?.let {{
                    Result.success(it.toDomain())
                }} ?: Result.failure(Exception("Empty response"))
            }} else {{
                Result.failure(Exception("Error: ${{response.code()}}"))
            }}
        }} catch (e: Exception) {{
            Result.failure(e)
        }}
    }}
}}
"""

    def _generate_state(self) -> str:
        """Generate state classes."""
        return f"""package {self.package_name}.presentation.state

import {self.package_name}.domain.model.{self.feature_name}

// {self.spec.spec_id}: Screen state
data class {self.feature_name}State(
    val isLoading: Boolean = false,
    val data: {self.feature_name}? = null,
    val error: String? = null,
)

// {self.spec.spec_id}: User actions
sealed interface {self.feature_name}Action {{
    data class Load(val id: String) : {self.feature_name}Action
}}

// {self.spec.spec_id}: One-time events
sealed interface {self.feature_name}Event {{
    data class ShowError(val message: String) : {self.feature_name}Event
}}
"""

    def _generate_viewmodel(self) -> str:
        """Generate ViewModel."""
        return f"""package {self.package_name}.presentation.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import {self.package_name}.domain.usecase.Get{self.feature_name}UseCase
import {self.package_name}.presentation.state.{self.feature_name}Action
import {self.package_name}.presentation.state.{self.feature_name}Event
import {self.package_name}.presentation.state.{self.feature_name}State
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

// {self.spec.spec_id}: ViewModel
@HiltViewModel
class {self.feature_name}ViewModel @Inject constructor(
    private val get{self.feature_name}UseCase: Get{self.feature_name}UseCase,
) : ViewModel() {{

    private val _state = MutableStateFlow({self.feature_name}State())
    val state: StateFlow<{self.feature_name}State> = _state.asStateFlow()

    private val _events = Channel<{self.feature_name}Event>()
    val events = _events.receiveAsFlow()

    fun onAction(action: {self.feature_name}Action) {{
        when (action) {{
            is {self.feature_name}Action.Load -> load(action.id)
        }}
    }}

    private fun load(id: String) {{
        viewModelScope.launch {{
            _state.update {{ it.copy(isLoading = true, error = null) }}

            get{self.feature_name}UseCase(id)
                .onSuccess {{ data ->
                    _state.update {{ it.copy(isLoading = false, data = data) }}
                }}
                .onFailure {{ error ->
                    _state.update {{ it.copy(isLoading = false, error = error.message) }}
                    _events.send({self.feature_name}Event.ShowError(error.message ?: "Unknown error"))
                }}
        }}
    }}
}}
"""

    def _generate_screen(self) -> str:
        """Generate Compose screen."""
        return f"""package {self.package_name}.presentation.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import {self.package_name}.presentation.state.{self.feature_name}Action
import {self.package_name}.presentation.state.{self.feature_name}Event
import {self.package_name}.presentation.viewmodel.{self.feature_name}ViewModel

// {self.spec.spec_id}: Screen
@Composable
fun {self.feature_name}Screen(
    viewModel: {self.feature_name}ViewModel = hiltViewModel(),
) {{
    val state by viewModel.state.collectAsStateWithLifecycle()

    LaunchedEffect(Unit) {{
        viewModel.events.collect {{ event ->
            when (event) {{
                is {self.feature_name}Event.ShowError -> {{
                    // TODO: Show snackbar or toast
                }}
            }}
        }}
    }}

    {self.feature_name}Content(
        state = state,
        onAction = viewModel::onAction,
    )
}}

@Composable
private fun {self.feature_name}Content(
    state: {self.spec.feature.replace(" ", "")}State,
    onAction: ({self.feature_name}Action) -> Unit,
) {{
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center,
    ) {{
        when {{
            state.isLoading -> CircularProgressIndicator()
            state.error != null -> Text("Error: ${{state.error}}")
            state.data != null -> Text("Data: ${{state.data}}")
            else -> Text("No data")
        }}
    }}
}}
"""

    def _generate_unit_tests(self) -> str:
        """Generate unit tests."""
        return f"""package {self.package_name}.domain

import {self.package_name}.domain.model.{self.feature_name}
import {self.package_name}.domain.repository.{self.feature_name}Repository
import {self.package_name}.domain.usecase.Get{self.feature_name}UseCase
import kotlinx.coroutines.test.runTest
import org.junit.Before
import org.junit.Test
import org.mockito.Mock
import org.mockito.Mockito.`when`
import org.mockito.MockitoAnnotations
import kotlin.test.assertTrue

// TEST-{self.spec.spec_id}-U-01: Test Get{self.feature_name}UseCase
class {self.feature_name}UseCaseTest {{

    @Mock
    private lateinit var repository: {self.feature_name}Repository

    private lateinit var useCase: Get{self.feature_name}UseCase

    @Before
    fun setup() {{
        MockitoAnnotations.openMocks(this)
        useCase = Get{self.feature_name}UseCase(repository)
    }}

    @Test
    fun `get {self.feature_name.lower()} returns success`() = runTest {{
        // Given
        val id = "test-id"
        val expected{self.feature_name} = {self.feature_name}(id = id)
        `when`(repository.get{self.feature_name}(id)).thenReturn(Result.success(expected{self.feature_name}))

        // When
        val result = useCase(id)

        // Then
        assertTrue(result.isSuccess)
    }}
}}
"""


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Code Builder - Generate Android code from SPEC")
    parser.add_argument("command", choices=["generate"], help="Command to execute")
    parser.add_argument("spec_file", help="Path to SPEC.md file")
    parser.add_argument("--output", "-o", help="Output directory", default="./generated")
    parser.add_argument("--package", "-p", help="Package name", default="com.example.app")

    args = parser.parse_args()

    # Parse SPEC
    spec_file = Path(args.spec_file)
    if not spec_file.exists():
        print(f"{Colors.FAIL}Error: SPEC file not found: {spec_file}{Colors.ENDC}")
        sys.exit(1)

    try:
        spec = SpecParser.parse(spec_file)
    except Exception as e:
        print(f"{Colors.FAIL}Error parsing SPEC: {e}{Colors.ENDC}")
        sys.exit(1)

    # Generate code
    output_dir = Path(args.output)
    generator = CodeGenerator(spec, output_dir)
    generator.package_name = args.package

    if args.command == "generate":
        generator.generate_all()


if __name__ == "__main__":
    main()
