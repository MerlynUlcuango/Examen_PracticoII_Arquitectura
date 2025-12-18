package com.banquito.cbs.dto.response;

import lombok.Getter;
import lombok.Setter;

import java.time.LocalDate;

@Getter
@Setter
public class BranchHolidayResponse {

    private LocalDate date;
    private String name;
}
