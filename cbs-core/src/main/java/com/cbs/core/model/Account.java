package com.cbs.core.model;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.io.Serializable;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Account implements Serializable {
    private static final long serialVersionUID = 1L;

    private String accountId;
    private String customerId;
    private String accountType; // CURRENT, SAVINGS, TERM, CORPORATE
    private String currency; // EUR, USD, etc.
    private BigDecimal balance;
    private BigDecimal availableBalance;
    private String status; // ACTIVE, BLOCKED, CLOSED
    private String iban;
    private String bic;
    
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime createdAt;
    
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime lastModified;
    
    private BigDecimal interestRate;
    private String productCode;
}
