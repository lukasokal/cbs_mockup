package com.cbs.account.controller;

import com.cbs.account.service.AccountService;
import com.cbs.core.dto.ApiResponse;
import com.cbs.core.model.Account;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/accounts")
@Slf4j
@CrossOrigin(origins = "*", maxAge = 3600)
public class AccountController {

    private final AccountService accountService;

    public AccountController(AccountService accountService) {
        this.accountService = accountService;
    }

    @PostMapping
    public ResponseEntity<ApiResponse<Account>> createAccount(@RequestBody Account account) {
        log.info("CREATE account request for customer: {}", account.getCustomerId());
        try {
            Account createdAccount = accountService.createAccount(account);
            return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.success(createdAccount, "Account created successfully"));
        } catch (Exception e) {
            log.error("Error creating account", e);
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ApiResponse.error(400, "Failed to create account: " + e.getMessage()));
        }
    }

    @GetMapping("/{accountId}")
    public ResponseEntity<ApiResponse<Account>> getAccount(@PathVariable String accountId) {
        log.info("GET account: {}", accountId);
        return accountService.getAccount(accountId)
            .map(account -> ResponseEntity.ok(ApiResponse.success(account)))
            .orElse(ResponseEntity.status(HttpStatus.NOT_FOUND)
                .body(ApiResponse.error(404, "Account not found")));
    }

    @GetMapping("/customer/{customerId}")
    public ResponseEntity<ApiResponse<List<Account>>> getCustomerAccounts(@PathVariable String customerId) {
        log.info("GET accounts for customer: {}", customerId);
        List<Account> accounts = accountService.getAccountsByCustomer(customerId);
        return ResponseEntity.ok(ApiResponse.success(accounts, "Accounts retrieved successfully"));
    }

    @PutMapping("/{accountId}")
    public ResponseEntity<ApiResponse<Account>> updateAccount(
            @PathVariable String accountId,
            @RequestBody Account account) {
        log.info("UPDATE account: {}", accountId);
        try {
            Account updatedAccount = accountService.updateAccount(accountId, account);
            return ResponseEntity.ok(ApiResponse.success(updatedAccount, "Account updated successfully"));
        } catch (Exception e) {
            log.error("Error updating account", e);
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ApiResponse.error(400, "Failed to update account: " + e.getMessage()));
        }
    }

    @DeleteMapping("/{accountId}")
    public ResponseEntity<ApiResponse<Void>> deleteAccount(@PathVariable String accountId) {
        log.info("DELETE account: {}", accountId);
        try {
            accountService.deleteAccount(accountId);
            return ResponseEntity.ok(ApiResponse.success(null, "Account deleted successfully"));
        } catch (Exception e) {
            log.error("Error deleting account", e);
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ApiResponse.error(400, "Failed to delete account: " + e.getMessage()));
        }
    }

    @PostMapping("/{accountId}/debit")
    public ResponseEntity<ApiResponse<String>> debitAccount(
            @PathVariable String accountId,
            @RequestParam String amount) {
        log.info("DEBIT account {} with amount {}", accountId, amount);
        try {
            accountService.debitAccount(accountId, new java.math.BigDecimal(amount));
            return ResponseEntity.ok(ApiResponse.success("", "Account debited successfully"));
        } catch (Exception e) {
            log.error("Error debiting account", e);
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ApiResponse.error(400, "Failed to debit account: " + e.getMessage()));
        }
    }

    @PostMapping("/{accountId}/credit")
    public ResponseEntity<ApiResponse<String>> creditAccount(
            @PathVariable String accountId,
            @RequestParam String amount) {
        log.info("CREDIT account {} with amount {}", accountId, amount);
        try {
            accountService.creditAccount(accountId, new java.math.BigDecimal(amount));
            return ResponseEntity.ok(ApiResponse.success("", "Account credited successfully"));
        } catch (Exception e) {
            log.error("Error crediting account", e);
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ApiResponse.error(400, "Failed to credit account: " + e.getMessage()));
        }
    }

    @GetMapping("/health")
    public ResponseEntity<String> health() {
        return ResponseEntity.ok("Account Service is running");
    }
}
