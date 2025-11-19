# Validate SPEC Documents

Validates all SPEC documents in the project for completeness and correctness.

## What This Command Does

Runs the SPEC validation tool to check:
- SPEC document structure and frontmatter
- Required sections presence
- EARS format requirements
- Traceability matrix completeness
- Related skills references
- Implementation checklist status

## Running Validation

```bash
# Validate all SPEC documents
python3 tools/validate_specs.py --all

# Validate specific SPEC
python3 tools/validate_specs.py --spec SPEC-001

# Validate with detailed output
python3 tools/validate_specs.py --all --verbose
```

## Common Issues and Fixes

### Missing Requirements
**Issue**: SPEC has no requirements defined
**Fix**: Add at least one requirement in EARS format

### Incomplete Traceability
**Issue**: Requirements not linked to code files
**Fix**: Update traceability matrix with implementation details

### Invalid SPEC ID
**Issue**: SPEC ID format is incorrect
**Fix**: Use format `SPEC-XXX` (e.g., SPEC-001, SPEC-002)

### Missing Frontmatter
**Issue**: SPEC document missing YAML frontmatter
**Fix**: Add frontmatter with spec_id, feature, status, version, etc.

## After Validation

If validation passes:
- ✅ SPEC is ready for implementation
- Continue with feature development

If validation fails:
- ❌ Fix the reported issues
- Re-run validation
- Commit fixes: `git commit -m "docs(SPEC-XXX): Fix validation issues"`

---

**Running validation now...**
