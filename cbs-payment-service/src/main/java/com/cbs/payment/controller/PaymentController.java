package com.cbs.payment.controller;

import com.cbs.core.dto.ApiResponse;
import com.cbs.core.model.Payment;
import com.cbs.payment.service.PaymentService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/payments")
@Slf4j
@CrossOrigin(origins = "${CORS_ALLOWED_ORIGINS:http://localhost:3000}", maxAge = 3600)
public class PaymentController {

    private final PaymentService paymentService;

    public PaymentController(PaymentService paymentService) {
        this.paymentService = paymentService;
    }

    @PostMapping
    public ResponseEntity<ApiResponse<Payment>> initiatePayment(@RequestBody Payment payment) {
        log.info("INITIATE payment from account: {}", payment.getInitiatorAccountId());
        try {
            Payment initiatedPayment = paymentService.initiatePayment(payment);
            return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.success(initiatedPayment, "Payment initiated successfully"));
        } catch (Exception e) {
            log.error("Error initiating payment", e);
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ApiResponse.error(400, "Failed to initiate payment: " + e.getMessage()));
        }
    }

    @GetMapping("/{paymentId}")
    public ResponseEntity<ApiResponse<Payment>> getPayment(@PathVariable String paymentId) {
        log.info("GET payment: {}", paymentId);
        return paymentService.getPayment(paymentId)
            .map(payment -> ResponseEntity.ok(ApiResponse.success(payment)))
            .orElse(ResponseEntity.status(HttpStatus.NOT_FOUND)
                .body(ApiResponse.error(404, "Payment not found")));
    }

    @GetMapping("/account/{accountId}")
    public ResponseEntity<ApiResponse<List<Payment>>> getPaymentsByAccount(@PathVariable String accountId) {
        log.info("GET payments for account: {}", accountId);
        List<Payment> payments = paymentService.getPaymentsByAccount(accountId);
        return ResponseEntity.ok(ApiResponse.success(payments, "Payments retrieved successfully"));
    }

    @GetMapping("/status/{status}")
    public ResponseEntity<ApiResponse<List<Payment>>> getPaymentsByStatus(@PathVariable String status) {
        log.info("GET payments with status: {}", status);
        List<Payment> payments = paymentService.getPaymentsByStatus(status);
        return ResponseEntity.ok(ApiResponse.success(payments, "Payments retrieved successfully"));
    }

    @PostMapping("/{paymentId}/submit")
    public ResponseEntity<ApiResponse<Payment>> submitPayment(@PathVariable String paymentId) {
        log.info("SUBMIT payment: {}", paymentId);
        try {
            Payment payment = paymentService.submitPayment(paymentId);
            return ResponseEntity.ok(ApiResponse.success(payment, "Payment submitted successfully"));
        } catch (Exception e) {
            log.error("Error submitting payment", e);
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ApiResponse.error(400, "Failed to submit payment: " + e.getMessage()));
        }
    }

    @PostMapping("/{paymentId}/approve")
    public ResponseEntity<ApiResponse<Payment>> approvePayment(@PathVariable String paymentId) {
        log.info("APPROVE payment: {}", paymentId);
        try {
            Payment payment = paymentService.approvePayment(paymentId);
            return ResponseEntity.ok(ApiResponse.success(payment, "Payment approved successfully"));
        } catch (Exception e) {
            log.error("Error approving payment", e);
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ApiResponse.error(400, "Failed to approve payment: " + e.getMessage()));
        }
    }

    @PostMapping("/{paymentId}/reject")
    public ResponseEntity<ApiResponse<Payment>> rejectPayment(
            @PathVariable String paymentId,
            @RequestParam String reason) {
        log.info("REJECT payment {}: {}", paymentId, reason);
        try {
            Payment payment = paymentService.rejectPayment(paymentId, reason);
            return ResponseEntity.ok(ApiResponse.success(payment, "Payment rejected successfully"));
        } catch (Exception e) {
            log.error("Error rejecting payment", e);
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ApiResponse.error(400, "Failed to reject payment: " + e.getMessage()));
        }
    }

    @GetMapping("/health")
    public ResponseEntity<String> health() {
        return ResponseEntity.ok("Payment Service is running");
    }
}
