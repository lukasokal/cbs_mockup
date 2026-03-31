package com.cbs.payment.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import jakarta.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.time.LocalDate;

@Entity
@Table(name = "payments", schema = "public")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class PaymentEntity {
    
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(name = "payment_id")
    private String paymentId;
    
    @Column(name = "initiator_account_id", nullable = false)
    private String initiatorAccountId;
    
    @Column(name = "beneficiary_iban", nullable = false)
    private String beneficiaryIban;
    
    @Column(name = "beneficiary_name")
    private String beneficiaryName;
    
    @Column(name = "amount", precision = 19, scale = 2, nullable = false)
    private BigDecimal amount;
    
    @Column(name = "currency")
    private String currency;
    
    @Column(name = "payment_type")
    private String paymentType;
    
    @Column(name = "payment_status")
    private String paymentStatus;
    
    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    @Column(name = "executed_at")
    private LocalDateTime executedAt;
    
    @Column(name = "requested_execution_date")
    private LocalDate requestedExecutionDate;
    
    @Column(name = "remittance_information")
    private String remittanceInformation;
    
    @Column(name = "purpose_code")
    private String purposeCode;
    
    @Column(name = "end_to_end_reference")
    private String endToEndReference;
    
    @Column(name = "mandate_reference")
    private String mandateReference;
    
    @Column(name = "transaction_id")
    private String transactionId;
    
    @Column(name = "error_message")
    private String errorMessage;
    
    @Column(name = "beneficiary_bank_code")
    private String beneficiaryBankCode;
    
    @Column(name = "exchange_rate", precision = 10, scale = 4)
    private BigDecimal exchangeRate;
    
    @Column(name = "channel")
    private String channel;
    
    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        if (paymentStatus == null) {
            paymentStatus = "PENDING";
        }
    }
}
