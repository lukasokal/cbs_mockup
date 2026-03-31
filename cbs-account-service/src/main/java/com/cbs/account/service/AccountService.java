package com.cbs.account.service;

import com.cbs.account.entity.AccountEntity;
import com.cbs.account.repository.AccountRepository;
import com.cbs.core.model.Account;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
@Slf4j
public class AccountService {

    private final AccountRepository accountRepository;

    public AccountService(AccountRepository accountRepository) {
        this.accountRepository = accountRepository;
    }

    @Transactional
    public Account createAccount(Account account) {
        log.info("Creating account for customer: {}", account.getCustomerId());
        
        AccountEntity entity = new AccountEntity();
        entity.setCustomerId(account.getCustomerId());
        entity.setAccountType(account.getAccountType() != null ? account.getAccountType() : "CURRENT");
        entity.setCurrency(account.getCurrency() != null ? account.getCurrency() : "EUR");
        entity.setBalance(account.getBalance() != null ? account.getBalance() : BigDecimal.ZERO);
        entity.setAvailableBalance(entity.getBalance());
        entity.setStatus(account.getStatus() != null ? account.getStatus() : "ACTIVE");
        entity.setIban(account.getIban());
        entity.setBic(account.getBic());
        entity.setInterestRate(account.getInterestRate());
        entity.setProductCode(account.getProductCode());
        
        AccountEntity saved = accountRepository.save(entity);
        log.info("Account created with ID: {}", saved.getAccountId());
        
        return convertToModel(saved);
    }

    @Transactional(readOnly = true)
    public Optional<Account> getAccount(String accountId) {
        log.info("Fetching account: {}", accountId);
        return accountRepository.findByAccountId(accountId)
            .map(this::convertToModel);
    }

    @Transactional(readOnly = true)
    public List<Account> getAccountsByCustomer(String customerId) {
        log.info("Fetching accounts for customer: {}", customerId);
        return accountRepository.findByCustomerId(customerId)
            .stream()
            .map(this::convertToModel)
            .collect(Collectors.toList());
    }

    @Transactional
    public Account updateAccount(String accountId, Account account) {
        log.info("Updating account: {}", accountId);
        
        return accountRepository.findByAccountId(accountId)
            .map(existing -> {
                if (account.getStatus() != null) {
                    existing.setStatus(account.getStatus());
                }
                if (account.getBalance() != null) {
                    existing.setBalance(account.getBalance());
                    existing.setAvailableBalance(account.getBalance());
                }
                if (account.getInterestRate() != null) {
                    existing.setInterestRate(account.getInterestRate());
                }
                
                AccountEntity updated = accountRepository.save(existing);
                log.info("Account updated: {}", accountId);
                return convertToModel(updated);
            })
            .orElseThrow(() -> new RuntimeException("Account not found: " + accountId));
    }

    @Transactional
    public void debitAccount(String accountId, BigDecimal amount) {
        log.info("Debiting account {} with amount {}", accountId, amount);
        
        AccountEntity account = accountRepository.findByAccountId(accountId)
            .orElseThrow(() -> new RuntimeException("Account not found: " + accountId));
        
        if (account.getAvailableBalance().compareTo(amount) < 0) {
            throw new RuntimeException("Insufficient funds");
        }
        
        account.setBalance(account.getBalance().subtract(amount));
        account.setAvailableBalance(account.getAvailableBalance().subtract(amount));
        
        accountRepository.save(account);
    }

    @Transactional
    public void creditAccount(String accountId, BigDecimal amount) {
        log.info("Crediting account {} with amount {}", accountId, amount);
        
        AccountEntity account = accountRepository.findByAccountId(accountId)
            .orElseThrow(() -> new RuntimeException("Account not found: " + accountId));
        
        account.setBalance(account.getBalance().add(amount));
        account.setAvailableBalance(account.getAvailableBalance().add(amount));
        
        accountRepository.save(account);
    }

    @Transactional
    public void deleteAccount(String accountId) {
        log.info("Deleting account: {}", accountId);
        accountRepository.deleteById(accountId);
    }

    private Account convertToModel(AccountEntity entity) {
        Account account = new Account();
        account.setAccountId(entity.getAccountId());
        account.setCustomerId(entity.getCustomerId());
        account.setAccountType(entity.getAccountType());
        account.setCurrency(entity.getCurrency());
        account.setBalance(entity.getBalance());
        account.setAvailableBalance(entity.getAvailableBalance());
        account.setStatus(entity.getStatus());
        account.setIban(entity.getIban());
        account.setBic(entity.getBic());
        account.setCreatedAt(entity.getCreatedAt());
        account.setLastModified(entity.getLastModified());
        account.setInterestRate(entity.getInterestRate());
        account.setProductCode(entity.getProductCode());
        return account;
    }
}
