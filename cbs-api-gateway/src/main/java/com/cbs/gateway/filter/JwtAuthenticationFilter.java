package com.cbs.gateway.filter;

import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.gateway.filter.GatewayFilter;
import org.springframework.cloud.gateway.filter.factory.AbstractGatewayFilterFactory;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;

@Slf4j
@Component
public class JwtAuthenticationFilter extends AbstractGatewayFilterFactory<JwtAuthenticationFilter.Config> {

    @Value("${jwt.secret:cbs-secret-key-banking-system-2026}")
    private String secretKey;

    public JwtAuthenticationFilter() {
        super(Config.class);
    }

    @Override
    public GatewayFilter apply(Config config) {
        return (exchange, chain) -> {
            try {
                // Skip authentication for public endpoints
                if (isPublicEndpoint(exchange.getRequest().getPath().value())) {
                    return chain.filter(exchange);
                }

                String authHeader = exchange.getRequest().getHeaders().getFirst("Authorization");
                
                if (authHeader == null || !authHeader.startsWith("Bearer ")) {
                    return onError(exchange, "Missing or invalid token");
                }

                String token = authHeader.substring(7);
                
                try {
                    Jwts.parserBuilder()
                        .setSigningKey(secretKey.getBytes())
                        .build()
                        .parseClaimsJws(token);
                        
                    return chain.filter(exchange);
                } catch (SignatureException ex) {
                    log.error("Invalid JWT signature: {}", ex.getMessage());
                    return onError(exchange, "Invalid token");
                }
            } catch (Exception e) {
                log.error("Authentication error: {}", e.getMessage());
                return onError(exchange, "Authentication failed");
            }
        };
    }

    private boolean isPublicEndpoint(String path) {
        return path.contains("/auth/") || path.contains("/public/") || path.contains("/health");
    }

    private Mono<Void> onError(ServerWebExchange exchange, String message) {
        exchange.getResponse().setStatusCode(HttpStatus.UNAUTHORIZED);
        return exchange.getResponse().setComplete();
    }

    public static class Config {
    }
}
