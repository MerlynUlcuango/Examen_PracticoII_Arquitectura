package com.banquito.cbs.dto.request;

import jakarta.validation.constraints.NotBlank;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class BranchUpdatePhoneRequest {

    @NotBlank
    private String phoneNumber;
}
