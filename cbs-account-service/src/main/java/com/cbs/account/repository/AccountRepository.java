package com.cbs.account.repository;

import com.cbs.account.entity.AccountEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface AccountRepository extends JpaRepository<AccountEntity, String> {
    Optional<AccountEntity> findByIban(String iban);
    List<AccountEntity> findByCustomerId(String customerId);
    List<AccountEntity> findByCustomerIdAndStatus(String customerId, String status);
    Optional<AccountEntity> findByAccountId(String accountId);
    List<AccountEntity> findByStatus(String status);
}
