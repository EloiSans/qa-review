# qa-review

# Architecture
## MVC
## Hexagonal
![](https://www.arhohuttunen.com/media/post/hexagonal-architecture/hexagonal-architecture-external-dependencies.svg)

| **When to Implement Hexagonal Architecture**                             | **When Not to Implement Hexagonal Architecture**                            |
|--------------------------------------------------------------------------|----------------------------------------------------------------------------|
| **Long-lived, complex applications** that need to be maintainable and flexible over time (e.g., enterprise applications). | **Small, simple projects** that do not require complex abstractions (e.g., a simple CRUD app or a small internal tool). |
| **High-change environments**, where external systems (e.g., databases, APIs, messaging systems) are expected to evolve frequently. | **Low-change, stable systems** that interact with a single external system and don’t expect future changes (e.g., legacy internal systems). |
| **Testing priority**: Applications that require extensive unit testing and need to isolate core business logic from external dependencies (via mocks/stubs). | **Prototyping or MVPs** where speed is more important than flexibility, and future changes are not yet a concern. |
| **Microservices** or **distributed systems**, where clean separation of concerns between internal logic and external systems is important. | **Tight deadlines** where setting up ports and adapters may slow down development unnecessarily for short-term goals. |
| Applications where you want the **core logic to be technology-agnostic**, allowing easy substitution of external dependencies (e.g., switching databases). | **Performance-critical applications** where extra layers of abstraction could introduce unnecessary runtime overhead (e.g., real-time systems). |
| **Team scalability**: Projects where different teams are working on different parts (e.g., core logic vs adapters), encouraging modularity and independence. | Projects developed by a team that **lacks experience** or **familiarity** with Hexagonal Architecture, risking misuse or overcomplication. |

# Integration Testing Tools
## Mail Testing
MailPit

## SMS Testing
LocalStack and MockSMS

## API Contracts Testing
PactIO

## Storage Testing
MinIO provides a simple and efficient way to mock AWS S3 for integration testing. By running a local MinIO server, you can simulate real-world S3 operations in your development and CI pipelines without relying on AWS infrastructure.
