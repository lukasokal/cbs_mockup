package com.cbs.payment.repository;

import com.cbs.payment.entity.PaymentEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface PaymentRepository extends JpaRepository<PaymentEntity, String> {
    Optional<PaymentEntity> findByPaymentId(String paymentId);
    List<PaymentEntity> findByInitiatorAccountId(String initiatorAccountId);
    List<PaymentEntity> findByPaymentStatus(String paymentStatus);
    List<PaymentEntity> findByInitiatorAccountIdAndPaymentStatus(String initiatorAccountId, String paymentStatus);
    Optional<PaymentEntity> findByEndToEndReference(String endToEndReference);
}
