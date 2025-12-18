package com.banquito.cbs.dto.request;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class BranchCreateRequest {

    @NotBlank
    private String id; 

    @Email
    @NotBlank
    private String emailAddress;

    @NotBlank
    private String name;

    @NotBlank
    private String phoneNumber;
}
