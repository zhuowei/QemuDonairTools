@import Darwin;

volatile bool startthread;
void* dothethread(void* start) {
    while (!startthread) {
        usleep(100);
    }
    *(volatile uint64_t*)0x4141deadbee0 = 0x1234;
#if 0
    if (*(volatile uint64_t*)0x4141deadbee0 == 0x1) {
        printf("hey\n");
    }
#endif
    return nil;
}

#pragma pack(4)
typedef struct {
    mach_msg_header_t Head;
    mach_msg_body_t msgh_body;
    mach_msg_port_descriptor_t thread;
    mach_msg_port_descriptor_t task;
    NDR_record_t NDR;
    uint32_t exception;
    uint32_t codeCnt;
    mach_exception_data_type_t code[2];
} exception_raise_request; // the bits we need at least

typedef struct {
    mach_msg_header_t Head;
    NDR_record_t NDR;
    kern_return_t RetCode;
} exception_raise_reply;
#pragma pack()

static boolean_t donair_exception_server(mach_msg_header_t *InHeadP, mach_msg_header_t *OutHeadP) {
    exception_raise_request* req = (exception_raise_request*)InHeadP;
    __builtin_dump_struct(req, &printf);
    printf("%lx %x %x %x %llx %llx\n", sizeof(exception_raise_request), req->Head.msgh_size, req->exception, req->codeCnt, req->code[0], req->code[1]);
    return true;
}

int main() {
    pthread_t thread;
    pthread_create(&thread, nil, dothethread, nil);
    mach_port_t target_thread = pthread_mach_thread_np(thread);
    mach_port_t exc_port = 0;
    if (mach_port_allocate(mach_task_self_, MACH_PORT_RIGHT_RECEIVE, &exc_port) != KERN_SUCCESS) {
        abort();
    }
    if (mach_port_insert_right(mach_task_self_, exc_port, exc_port, MACH_MSG_TYPE_MAKE_SEND) != KERN_SUCCESS) {
        abort();
    }
    if (thread_set_exception_ports(
        target_thread,
        EXC_MASK_BAD_ACCESS | EXC_MASK_BAD_INSTRUCTION | EXC_MASK_ARITHMETIC | EXC_MASK_BREAKPOINT,
        exc_port,
        MACH_EXCEPTION_CODES | EXCEPTION_DEFAULT,
        ARM_THREAD_STATE64) != KERN_SUCCESS) {
        abort();
    }
    startthread = true;
    if (mach_msg_server_once(donair_exception_server, 4096, exc_port, 0) != KERN_SUCCESS) {
        fprintf(stderr, "fail! mach_msg_server_once\n");
        exit(1);
    }
    arm_exception_state64_t exception_state;
    uint32_t exception_count = ARM_EXCEPTION_STATE64_COUNT;
    if (thread_get_state(target_thread, ARM_EXCEPTION_STATE64, (thread_state_t)&exception_state, &exception_count) != KERN_SUCCESS) {
        fprintf(stderr, "fail! thread_get_state\n");
        exit(1);
    }
    __builtin_dump_struct(&exception_state, printf);
}