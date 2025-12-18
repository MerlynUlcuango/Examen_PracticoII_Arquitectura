package com.banquito.cbs.service;

import com.banquito.cbs.dto.request.BranchCreateRequest;
import com.banquito.cbs.dto.request.BranchHolidayCreateRequest;
import com.banquito.cbs.dto.request.BranchUpdatePhoneRequest;
import com.banquito.cbs.model.Branch;
import com.banquito.cbs.model.BranchHoliday;

import java.time.LocalDate;
import java.util.List;

public interface BranchService {

    List<Branch> getAllBranches();
    Branch createBranch(BranchCreateRequest request);
    Branch getBranchById(Integer id);
    Branch updateBranchPhone(Integer id, BranchUpdatePhoneRequest request);

    Branch addHoliday(Integer id, BranchHolidayCreateRequest request);
    Branch removeHoliday(Integer id, LocalDate date);
    List<BranchHoliday> getHolidays(Integer id);
    boolean isHoliday(Integer id, LocalDate date);
}
