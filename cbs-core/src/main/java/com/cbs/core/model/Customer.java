package com.cbs.core.model;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.io.Serializable;
import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Customer implements Serializable {
    private static final long serialVersionUID = 1L;

    private String customerId;
    private String firstName;
    private String lastName;
    private String email;
    private String phoneNumber;
    private String customerType; // INDIVIDUAL, CORPORATE
    private String identificationNumber; // SSN or Tax ID
    private String identificationDocType; // PASSPORT, ID_CARD, DRIVER_LICENSE
    private String status; // ACTIVE, BLOCKED, CLOSED
    private String kycStatus; // PENDING, APPROVED, REJECTED
    
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime createdAt;
    
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime lastModified;
    
    private String country;
    private String city;
    private String address;
    private String postalCode;
    private String riskRating; // LOW, MEDIUM, HIGH, CRITICAL
    private boolean pepMatch;
    private boolean sanctionMatch;
}
