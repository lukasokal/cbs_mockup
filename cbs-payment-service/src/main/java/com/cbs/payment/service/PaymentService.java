package com.cbs.payment.service;

import com.cbs.core.model.Payment;
import com.cbs.payment.entity.PaymentEntity;
import com.cbs.payment.repository.PaymentRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
@Slf4j
public class PaymentService {

    private final PaymentRepository paymentRepository;
    private final KafkaTemplate<String, Object> kafkaTemplate;

    public PaymentService(PaymentRepository paymentRepository, KafkaTemplate<String, Object> kafkaTemplate) {
        this.paymentRepository = paymentRepository;
        this.kafkaTemplate = kafkaTemplate;
    }

    @Transactional
    public Payment initiatePayment(Payment payment) {
        log.info("Initiating payment from account {} to {}", payment.getInitiatorAccountId(), payment.getBeneficiaryIban());
        
        PaymentEntity entity = new PaymentEntity();
        entity.setInitiatorAccountId(payment.getInitiatorAccountId());
        entity.setBeneficiaryIban(payment.getBeneficiaryIban());
        entity.setBeneficiaryName(payment.getBeneficiaryName());
        entity.setAmount(payment.getAmount());
        entity.setCurrency(payment.getCurrency() != null ? payment.getCurrency() : "EUR");
        entity.setPaymentType(payment.getPaymentType() != null ? payment.getPaymentType() : "SEPA_SCT");
        entity.setPaymentStatus("PENDING");
        entity.setRemittanceInformation(payment.getRemittanceInformation());
        entity.setPurposeCode(payment.getPurposeCode());
        entity.setEndToEndReference(payment.getEndToEndReference());
        entity.setChannel(payment.getChannel() != null ? payment.getChannel() : "WEB");
        entity.setRequestedExecutionDate(payment.getRequestedExecutionDate());
        
        PaymentEntity saved = paymentRepository.save(entity);
        log.info("Payment initiated with ID: {}", saved.getPaymentId());
        
        // Publish event to Kafka
        publishPaymentEvent("payment-initiated", convertToModel(saved));
        
        return convertToModel(saved);
    }

    @Transactional
    public Payment submitPayment(String paymentId) {
        log.info("Submitting payment: {}", paymentId);
        
        return paymentRepository.findByPaymentId(paymentId)
            .map(payment -> {
                payment.setPaymentStatus("SUBMITTED");
                PaymentEntity updated = paymentRepository.save(payment);
                
                // Publish event
                publishPaymentEvent("payment-submitted", convertToModel(updated));
                
                log.info("Payment submitted: {}", paymentId);
                return convertToModel(updated);
            })
            .orElseThrow(() -> new RuntimeException("Payment not found: " + paymentId));
    }

    @Transactional
    public Payment approvePayment(String paymentId) {
        log.info("Approving payment: {}", paymentId);
        
        return paymentRepository.findByPaymentId(paymentId)
            .map(payment -> {
                payment.setPaymentStatus("ACCEPTED");
                payment.setExecutedAt(LocalDateTime.now());
                PaymentEntity updated = paymentRepository.save(payment);
                
                // Publish event
                publishPaymentEvent("payment-accepted", convertToModel(updated));
                
                log.info("Payment approved: {}", paymentId);
                return convertToModel(updated);
            })
            .orElseThrow(() -> new RuntimeException("Payment not found: " + paymentId));
    }

    @Transactional
    public Payment rejectPayment(String paymentId, String reason) {
        log.info("Rejecting payment {}: {}", paymentId, reason);
        
        return paymentRepository.findByPaymentId(paymentId)
            .map(payment -> {
                payment.setPaymentStatus("REJECTED");
                payment.setErrorMessage(reason);
                PaymentEntity updated = paymentRepository.save(payment);
                
                // Publish event
                publishPaymentEvent("payment-rejected", convertToModel(updated));
                
                log.info("Payment rejected: {}", paymentId);
                return convertToModel(updated);
            })
            .orElseThrow(() -> new RuntimeException("Payment not found: " + paymentId));
    }

    @Transactional(readOnly = true)
    public Optional<Payment> getPayment(String paymentId) {
        log.info("Fetching payment: {}", paymentId);
        return paymentRepository.findByPaymentId(paymentId)
            .map(this::convertToModel);
    }

    @Transactional(readOnly = true)
    public List<Payment> getPaymentsByAccount(String accountId) {
        log.info("Fetching payments for account: {}", accountId);
        return paymentRepository.findByInitiatorAccountId(accountId)
            .stream()
            .map(this::convertToModel)
            .collect(Collectors.toList());
    }

    @Transactional(readOnly = true)
    public List<Payment> getPaymentsByStatus(String status) {
        log.info("Fetching payments with status: {}", status);
        return paymentRepository.findByPaymentStatus(status)
            .stream()
            .map(this::convertToModel)
            .collect(Collectors.toList());
    }

    private void publishPaymentEvent(String eventType, Payment payment) {
        try {
            kafkaTemplate.send("payment-events", eventType, payment);
            log.debug("Event published: {} for payment {}", eventType, payment.getPaymentId());
        } catch (Exception e) {
            log.warn("Failed to publish event: {}", e.getMessage());
        }
    }

    private Payment convertToModel(PaymentEntity entity) {
        Payment payment = new Payment();
        payment.setPaymentId(entity.getPaymentId());
        payment.setInitiatorAccountId(entity.getInitiatorAccountId());
        payment.setBeneficiaryIban(entity.getBeneficiaryIban());
        payment.setBeneficiaryName(entity.getBeneficiaryName());
        payment.setAmount(entity.getAmount());
        payment.setCurrency(entity.getCurrency());
        payment.setPaymentType(entity.getPaymentType());
        payment.setPaymentStatus(entity.getPaymentStatus());
        payment.setCreatedAt(entity.getCreatedAt());
        payment.setExecutedAt(entity.getExecutedAt());
        payment.setRequestedExecutionDate(entity.getRequestedExecutionDate());
        payment.setRemittanceInformation(entity.getRemittanceInformation());
        payment.setPurposeCode(entity.getPurposeCode());
        payment.setEndToEndReference(entity.getEndToEndReference());
        payment.setMandateReference(entity.getMandateReference());
        payment.setTransactionId(entity.getTransactionId());
        payment.setErrorMessage(entity.getErrorMessage());
        payment.setBeneficiaryBankCode(entity.getBeneficiaryBankCode());
        payment.setExchangeRate(entity.getExchangeRate());
        payment.setChannel(entity.getChannel());
        return payment;
    }
}
