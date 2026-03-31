package com.cbs.middleware.service;

import com.cbs.core.model.Payment;
import com.cbs.core.model.Transaction;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Service
@Slf4j
public class FraudDetectionService {

    private final KafkaTemplate<String, Object> kafkaTemplate;
    
    // Fraud detection thresholds
    private static final BigDecimal HIGH_AMOUNT_THRESHOLD = new BigDecimal("10000.00");
    private static final BigDecimal SUSPICIOUS_AMOUNT_THRESHOLD = new BigDecimal("50000.00");

    public FraudDetectionService(KafkaTemplate<String, Object> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    public void analyzePayment(Payment payment) {
        log.info("Analyzing payment {} for fraud risk", payment.getPaymentId());

        int riskScore = 0;
        StringBuilder riskFactors = new StringBuilder();

        // Check amount risk
        if (payment.getAmount().compareTo(SUSPICIOUS_AMOUNT_THRESHOLD) > 0) {
            riskScore += 50;
            riskFactors.append("Very high amount; ");
        } else if (payment.getAmount().compareTo(HIGH_AMOUNT_THRESHOLD) > 0) {
            riskScore += 25;
            riskFactors.append("High amount; ");
        }

        // Check payment type risk (SWIFT often higher risk)
        if ("SWIFT".equalsIgnoreCase(payment.getPaymentType())) {
            riskScore += 15;
            riskFactors.append("International payment; ");
        }

        // Check for new beneficiary (would need account history)
        if (payment.getBeneficiaryIban() == null || payment.getBeneficiaryIban().isEmpty()) {
            riskScore += 20;
            riskFactors.append("No beneficiary info; ");
        }

        log.info("Payment {} fraud risk score: {}", payment.getPaymentId(), riskScore);

        if (riskScore > 60) {
            publishFraudAlert(payment, "HIGH", riskScore, riskFactors.toString());
        } else if (riskScore > 30) {
            publishFraudAlert(payment, "MEDIUM", riskScore, riskFactors.toString());
        }
    }

    public void analyzeTransaction(Transaction transaction) {
        log.info("Analyzing transaction {} for fraud risk", transaction.getTransactionId());

        int riskScore = 0;

        // Check for unusual patterns
        if (transaction.getAmount().compareTo(new BigDecimal("5000.00")) > 0) {
            riskScore += 20;
        }

        // Check channel (ATM withdrawals at night could be suspicious)
        if ("ATM".equalsIgnoreCase(transaction.getChannel())) {
            riskScore += 10;
        }

        if (riskScore > 30) {
            log.warn("Suspicious transaction detected: {}", transaction.getTransactionId());
        }
    }

    private void publishFraudAlert(Payment payment, String riskLevel, int riskScore, String factors) {
        try {
            String alert = String.format(
                "Fraud Alert - Payment: %s, Risk Level: %s, Score: %d, Factors: %s",
                payment.getPaymentId(), riskLevel, riskScore, factors
            );
            
            kafkaTemplate.send("fraud-events", payment.getPaymentId(), alert);
            log.warn("Fraud alert published: {}", alert);
        } catch (Exception e) {
            log.error("Failed to publish fraud alert", e);
        }
    }
}
