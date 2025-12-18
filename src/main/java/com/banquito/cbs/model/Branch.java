package com.banquito.cbs.model;

import lombok.Getter;
import lombok.Setter;
import org.springframework.data.mongodb.core.mapping.Document;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Objects;

@Entity
@Table(name = "branch")
@Document(collection = "branch")
@Getter
@Setter
public class Branch {

    @Id
    @Column(name = "id")
    private Integer id;

    @Column(name = "email_address")
    private String emailAddress;

    @Column(name = "name")
    private String name;

    @Column(name = "phone_number")
    private String phoneNumber;

    @Column(name = "state")
    private String state;

    @Column(name = "creation_date")
    private LocalDateTime creationDate;

    @Column(name = "last_modified_date")
    private LocalDateTime lastModifiedDate;

    @Column(name = "branch_holidays")
    private List<BranchHoliday> branchHolidays;

    public Branch() {
    }

    public Branch(Integer id) {
        this.id = id;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Branch)) return false;
        Branch branch = (Branch) o;
        return Objects.equals(id, branch.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }

    @Override
    public String toString() {
        return "Branch{" +
                "id=" + id +
                ", emailAddress='" + emailAddress + '\'' +
                ", name='" + name + '\'' +
                ", phoneNumber='" + phoneNumber + '\'' +
                ", state='" + state + '\'' +
                ", creationDate=" + creationDate +
                ", lastModifiedDate=" + lastModifiedDate +
                ", branchHolidays=" + branchHolidays +
                '}';
    }
}
