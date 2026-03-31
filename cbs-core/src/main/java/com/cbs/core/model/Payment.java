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
public class Payment implements Serializable {
    private static final long serialVersionUID = 1L;

    private String paymentId;
    private String initiatorAccountId;
    private String beneficiaryIban;
    private String beneficiaryName;
    private BigDecimal amount;
    private String currency;
    private String paymentType; // SEPA_SCT, SEPA_SDD, SWIFT, INSTANT, LOCAL
    private String paymentStatus; // PENDING, SUBMITTED, ACCEPTED, REJECTED, CANCELLED
    
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime createdAt;
    
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime executedAt;
    
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd")
    private LocalDateTime requestedExecutionDate;
    
    private String remittanceInformation;
    private String purposeCode;
    private String endToEndReference;
    private String mandateReference; // For Direct Debit
    private String transactionId; // Linked to Transaction
    private String errorMessage;
    private String beneficiaryBankCode;
    private BigDecimal exchangeRate; // For multi-currency
    private String channel;
}
