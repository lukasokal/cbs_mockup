package com.cbs.gateway.config;

import com.cbs.gateway.filter.JwtAuthenticationFilter;
import org.springframework.cloud.gateway.route.RouteLocator;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class GatewayConfig {

    private final JwtAuthenticationFilter jwtAuthenticationFilter;

    public GatewayConfig(JwtAuthenticationFilter jwtAuthenticationFilter) {
        this.jwtAuthenticationFilter = jwtAuthenticationFilter;
    }

    @Bean
    public RouteLocator routes(RouteLocatorBuilder builder) {
        return builder.routes()
            // Account Service Routes
            .route("account-service", r -> r
                .path("/api/accounts/**")
                .filters(f -> f.addRequestHeader("X-Service-Name", "account-service"))
                .uri("lb://account-service"))
            
            // Payment Service Routes
            .route("payment-service", r -> r
                .path("/api/payments/**")
                .filters(f -> f.addRequestHeader("X-Service-Name", "payment-service"))
                .uri("lb://payment-service"))
            
            // Transaction Service Routes
            .route("transaction-service", r -> r
                .path("/api/transactions/**")
                .filters(f -> f.addRequestHeader("X-Service-Name", "transaction-service"))
                .uri("lb://transaction-service"))
            
            // Auth Service Routes (Public)
            .route("auth-service", r -> r
                .path("/api/auth/**")
                .uri("lb://auth-service"))
            
            // Customer Service Routes
            .route("customer-service", r -> r
                .path("/api/customers/**")
                .filters(f -> f.addRequestHeader("X-Service-Name", "customer-service"))
                .uri("lb://customer-service"))
            
            .build();
    }
}
