# Java / Kotlin (JVM)

**Detect:** `pom.xml`, `build.gradle`, `build.gradle.kts`. Java 21+ or Kotlin 2.x.

## Spelling the layout
- Packages `com.example.shop.orders.{domain,application,adapters.in.web,adapters.out.persistence}`. In Kotlin, `in` is a keyword, so use `adapters.inbound` / `adapters.outbound`.
- A modular monolith uses `com.example.shop.modules.<context>`, and its public entry is the `com.example.shop.modules.<context>.api` package. Everything else is package-private where the language allows (Java default visibility, Kotlin `internal` with Gradle modules).
- Composition root: `Application.java`/`Application.kt`, plus `config` classes in `adapters` that wire beans when using Spring.
- For compiler-enforced boundaries, use Gradle/Maven modules `orders-domain`, `orders-application` and `orders-adapters` with matching dependencies.

## Slice idioms
| Piece | Idiom |
|---|---|
| Id | Java `record OrderId(UUID value)`; Kotlin `@JvmInline value class OrderId(val value: UUID)` |
| Value object | Java `record Money(long cents, Currency currency)` with a compact constructor that validates; Kotlin `data class` with `init` checks |
| Aggregate | Class with private fields, static `draft(...)` / `restore(snapshot)`, no setters, `List.copyOf` for exposed collections |
| Domain error | `class DomainException extends RuntimeException { final String code; }` (Kotlin: `class DomainException(val code: String) : RuntimeException(code)`) |
| Port | `interface OrderRepository` in `domain` |
| Use case | Class with constructor-injected ports and `execute(PlaceOrderCommand)` returning `OrderId` |
| Inbound validation | Bean Validation (`@Valid`, `@NotNull`) on the web DTO in `adapters.in`, never on domain classes |
| Database | JPA entities (`@Entity`) or jOOQ records live in `adapters.out.persistence` and are mapped to domain objects there. Batch inserts for child rows. Query timeouts set in config |
| Tests | JUnit 5 + AssertJ; domain tests use no Spring context |

No Spring, JPA or Jackson annotations on domain or application classes.

## Install commands to report
List the dependencies to add to `build.gradle(.kts)` or `pom.xml` (for example `org.postgresql:postgresql`, `jakarta.validation:jakarta.validation-api`, JUnit 5). Add Spring Boot, Ktor, Micronaut or Quarkus only if named.

## Extra boundary tooling
ArchUnit `layeredArchitecture()` and `slices().should().notDependOnEachOther()` tests enforce the same rules.
