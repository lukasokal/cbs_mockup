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
public class Transaction implements Serializable {
    private static final long serialVersionUID = 1L;

    private String transactionId;
    private String fromAccountId;
    private String toAccountId;
    private BigDecimal amount;
    private String currency;
    private String transactionType; // CREDIT, DEBIT, TRANSFER
    private String status; // PENDING, COMPLETED, FAILED, CANCELLED
    private String description;
    private String referenceNumber;
    
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime transactionDate;
    
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime valueDate;
    
    private String remittanceInformation;
    private String chargeBearer; // CRED, DEBT, SHAR
    private BigDecimal feeAmount;
    private String channel; // WEB, MOBILE, ATM, SWIFT, SEPA
    private String requestId; // For idempotency
}
