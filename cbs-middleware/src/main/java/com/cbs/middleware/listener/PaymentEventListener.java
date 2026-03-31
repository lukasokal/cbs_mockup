package com.cbs.middleware.listener;

import com.cbs.core.model.Payment;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class PaymentEventListener {

    @KafkaListener(topics = "payment-events", groupId = "middleware-payment-group")
    public void handlePaymentEvent(String eventType, Payment payment) {
        log.info("Payment Event Received: {} - Payment ID: {}, Status: {}", 
            eventType, payment.getPaymentId(), payment.getPaymentStatus());
        
        switch (eventType) {
            case "payment-initiated":
                handlePaymentInitiated(payment);
                break;
            case "payment-submitted":
                handlePaymentSubmitted(payment);
                break;
            case "payment-accepted":
                handlePaymentAccepted(payment);
                break;
            case "payment-rejected":
                handlePaymentRejected(payment);
                break;
            default:
                log.warn("Unknown payment event type: {}", eventType);
        }
    }

    private void handlePaymentInitiated(Payment payment) {
        log.debug("Processing payment initiated event for: {}", payment.getPaymentId());
        // TODO: Execute compliance checks, fraud detection
    }

    private void handlePaymentSubmitted(Payment payment) {
        log.debug("Processing payment submitted event for: {}", payment.getPaymentId());
        // TODO: Route to appropriate payment scheme (SEPA, SWIFT, etc.)
    }

    private void handlePaymentAccepted(Payment payment) {
        log.debug("Processing payment accepted event for: {}", payment.getPaymentId());
        // TODO: Trigger account debiting, notification dispatch
    }

    private void handlePaymentRejected(Payment payment) {
        log.debug("Processing payment rejected event for: {}", payment.getPaymentId());
        log.warn("Payment rejected: {} - Reason: {}", payment.getPaymentId(), payment.getErrorMessage());
        // TODO: Send notification, rollback any pending operations
    }
}
