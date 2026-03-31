package com.cbs.account.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "accounts", schema = "public")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class AccountEntity {
    
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "account_id")
    private String accountId;
    
    @Column(name = "customer_id", nullable = false)
    private String customerId;
    
    @Column(name = "account_type")
    private String accountType;
    
    @Column(name = "currency")
    private String currency;
    
    @Column(name = "balance", precision = 19, scale = 2)
    private BigDecimal balance;
    
    @Column(name = "available_balance", precision = 19, scale = 2)
    private BigDecimal availableBalance;
    
    @Column(name = "status")
    private String status;
    
    @Column(name = "iban", unique = true)
    private String iban;
    
    @Column(name = "bic")
    private String bic;
    
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    @Column(name = "last_modified")
    private LocalDateTime lastModified;
    
    @Column(name = "interest_rate", precision = 5, scale = 4)
    private BigDecimal interestRate;
    
    @Column(name = "product_code")
    private String productCode;
    
    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        lastModified = LocalDateTime.now();
        if (status == null) {
            status = "ACTIVE";
        }
    }
    
    @PreUpdate
    protected void onUpdate() {
        lastModified = LocalDateTime.now();
    }
}
